from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import random
import sys
from datetime import datetime
import re
import asyncpg
import asyncio

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Database configuration
database_url = os.getenv('POSTGRES_URL')  # Using POSTGRES_URL from Vercel
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Enable connection health checks
    'pool_size': 5,  # Adjust based on your needs
    'max_overflow': 10
}

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'options': {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d
            },
            'correct_answer': self.correct_answer,
            'explanation': self.explanation
        }

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(10), nullable=False, unique=True)
    score = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Float, nullable=False)  # Time in seconds
    date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'name': self.name,
            'roll_number': self.roll_number,
            'score': self.score,
            'time_taken': self.time_taken,
            'date_completed': self.date_completed.strftime('%Y-%m-%d %H:%M:%S')
        }

def validate_roll_number(roll_number):
    pattern = r'^\d{2}(10[1-9]|110)[A-Z]\d{4}$'
    return bool(re.match(pattern, roll_number))

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        
        if not name or not roll_number:
            return render_template('register.html', error="Both fields are required!")
        
        if not validate_roll_number(roll_number):
            return render_template('register.html', error="Invalid roll number format! Use format: 23102A0057")
        
        # Check if roll number already exists
        existing_user = Score.query.filter_by(roll_number=roll_number).first()
        if existing_user and existing_user.name != name:
            return render_template('register.html', 
                error="This roll number is already registered to a different name. Please contact administrator if this is an error.")
        
        # If roll number exists but same name, allow login
        if existing_user and existing_user.name == name:
            session['user'] = {'name': name, 'roll_number': roll_number, 'start_time': datetime.utcnow().timestamp()}
            return redirect(url_for('index'))
        
        # New user
        session['user'] = {'name': name, 'roll_number': roll_number, 'start_time': datetime.utcnow().timestamp()}
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/api/questions')
def get_questions():
    if 'user' not in session:
        return jsonify({'error': 'User not registered'}), 401
    
    try:
        questions = Question.query.all()
        if not questions:
            return jsonify({'error': 'No questions found in database'}), 404
        random_questions = random.sample(questions, min(10, len(questions)))
        return jsonify([q.to_dict() for q in random_questions])
    except Exception as e:
        print(f"Error fetching questions: {e}", file=sys.stderr)
        return jsonify({'error': 'Failed to fetch questions'}), 500

@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    if 'user' not in session:
        return jsonify({'error': 'User not registered'}), 401
    
    try:
        data = request.json
        final_score = data.get('score', 0)
        end_time = datetime.utcnow().timestamp()
        time_taken = end_time - session['user']['start_time']
        
        # Check if user already has a score
        existing_score = Score.query.filter_by(roll_number=session['user']['roll_number']).first()
        
        if existing_score:
            # Update existing score if new score is better or time is better with same score
            if final_score > existing_score.score or (final_score == existing_score.score and time_taken < existing_score.time_taken):
                existing_score.score = final_score
                existing_score.time_taken = time_taken
                existing_score.date_completed = datetime.utcnow()
        else:
            # Create new score entry
            score = Score(
                name=session['user']['name'],
                roll_number=session['user']['roll_number'],
                score=final_score,
                time_taken=time_taken
            )
            db.session.add(score)
        
        db.session.commit()
        return jsonify({
            'message': 'Score submitted successfully',
            'isNewHighScore': not existing_score or final_score > existing_score.score
        })
    except Exception as e:
        print(f"Error submitting score: {e}", file=sys.stderr)
        return jsonify({'error': 'Failed to submit score'}), 500

@app.route('/scoreboard')
def scoreboard():
    try:
        # Get all scores ordered by score (desc) and time (asc)
        scores = Score.query.order_by(Score.score.desc(), Score.time_taken.asc()).all()
        
        # Calculate ranks with ties
        ranked_scores = []
        current_rank = 1
        previous_score = None
        previous_time = None
        
        for score in scores:
            if previous_score == score.score and previous_time == score.time_taken:
                # Same score and time as previous, keep same rank
                rank = current_rank - 1
            else:
                # Different score or time, assign new rank
                rank = current_rank
            
            ranked_scores.append({
                'rank': rank,
                'name': score.name,
                'roll_number': score.roll_number,
                'score': score.score,
                'time_taken': score.time_taken
            })
            
            previous_score = score.score
            previous_time = score.time_taken
            current_rank += 1
        
        return render_template('scoreboard.html', scores=ranked_scores)
    except Exception as e:
        print(f"Error fetching scoreboard: {e}", file=sys.stderr)
        return render_template('scoreboard.html', error="Failed to load scoreboard")

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    if 'user' not in session:
        return jsonify({'error': 'User not registered'}), 401
    
    try:
        data = request.json
        question_id = data.get('question_id')
        selected_answer = data.get('answer')
        
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        is_correct = selected_answer == question.correct_answer
        return jsonify({
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation
        })
    except Exception as e:
        print(f"Error checking answer: {e}", file=sys.stderr)
        return jsonify({'error': 'Failed to check answer'}), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            question_count = Question.query.count()
            print(f"Number of questions in database: {question_count}")
            if question_count == 0:
                print("Warning: No questions in database. Please run populate_db.py")
        except Exception as e:
            print(f"Database initialization error: {e}", file=sys.stderr)
            sys.exit(1)
    app.run(debug=True) 
