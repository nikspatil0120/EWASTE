from app import db, Question
from app import app

questions_data = [
    {
        "question": "Which country generated the most e-waste globally as of 2019?",
        "option_a": "India",
        "option_b": "China",
        "option_c": "USA",
        "option_d": "Ghana",
        "correct_answer": "C",
        "explanation": "USA tops the e-waste charts—because apparently, we upgrade our gadgets faster than we blink."
    },
    {
        "question": "Which of these items is considered e-waste?",
        "option_a": "Plastic bottle",
        "option_b": "Old smartphone",
        "option_c": "Banana peel",
        "option_d": "Broken chair",
        "correct_answer": "B",
        "explanation": "If it has a chip, screen, or makes your life easier with a charger – it's e-waste when you dump it."
    },
    {
        "question": "Which heavy metal is commonly found in e-waste and harmful to health?",
        "option_a": "Gold",
        "option_b": "Iron",
        "option_c": "Mercury",
        "option_d": "Aluminum",
        "correct_answer": "C",
        "explanation": "Mercury sounds cool (like a superhero name), but in e-waste, it's dangerous – toxic to humans and animals."
    },
    {
        "question": "Which of these can be recovered from e-waste?",
        "option_a": "Chocolate",
        "option_b": "Gold",
        "option_c": "Oxygen",
        "option_d": "Water",
        "correct_answer": "B",
        "explanation": "There's actual gold in phones! That's why e-waste is called urban mining. Your old phone is a mini treasure chest."
    },
    {
        "question": "Which part of an old computer is most likely to contain recyclable metals?",
        "option_a": "The screen",
        "option_b": "The keyboard",
        "option_c": "The motherboard",
        "option_d": "The mouse",
        "correct_answer": "C",
        "explanation": "It's the brain of the computer and a hotspot for valuable metals. Motherboards = moneyboards."
    },
    {
        "question": "I count your steps, read your texts, track your sleep, and still can't figure out why you're tired. What am I?",
        "option_a": "Smartphone",
        "option_b": "Smartwatch",
        "option_c": "Fitness tracker",
        "option_d": "Sleep monitor",
        "correct_answer": "B",
        "explanation": "A smartwatch is your wrist-bound personal assistant that tracks everything but still can't solve the mystery of your tiredness!"
    },
    {
        "question": "I knew every song you ever played… and now I'm tangled in your drawer like spaghetti. What am I?",
        "option_a": "USB cable",
        "option_b": "Earphones",
        "option_c": "Charger",
        "option_d": "Headphones",
        "correct_answer": "B",
        "explanation": "Earphones - the tangled mess in your drawer that once brought you musical joy!"
    },
    {
        "question": "I flip like a book, worked overtime for your assignments, streamed late-night binges, and now overheat if you even look at me. What am I?",
        "option_a": "Tablet",
        "option_b": "Laptop",
        "option_c": "Smartphone",
        "option_d": "E-reader",
        "correct_answer": "B",
        "explanation": "Your trusty laptop - the workhorse that's seen better days and now runs hot with just a glance!"
    },
    {
        "question": "I am your everything – camera, calculator, gaming console, alarm clock… What am I?",
        "option_a": "Smartphone",
        "option_b": "Tablet",
        "option_c": "Laptop",
        "option_d": "Smartwatch",
        "correct_answer": "A",
        "explanation": "Your smartphone - the Swiss Army knife of modern technology that does it all!"
    },
    {
        "question": "You only remember me when your phone hits 1%. I'm the most borrowed, most lost item in human history. What am I?",
        "option_a": "Power bank",
        "option_b": "Charger",
        "option_c": "Battery",
        "option_d": "USB cable",
        "correct_answer": "B",
        "explanation": "The humble charger - always in demand, never where you left it, and your phone's best friend at 1%!"
    }
]

def populate_database():
    with app.app_context():
        # Clear existing questions
        Question.query.delete()
        
        # Add new questions
        for q in questions_data:
            question = Question(**q)
            db.session.add(question)
        
        db.session.commit()
        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database() 