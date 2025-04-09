# E-Waste Quiz Application

A modern web-based quiz application focused on e-waste awareness, featuring a beautiful green and white theme.

## Features

- Interactive quiz interface
- Real-time feedback on answers
- Detailed explanations for each question
- Progress tracking
- Responsive design
- PostgreSQL database integration

## Prerequisites

- Python 3.7 or higher
- PostgreSQL
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd ewaste-quiz
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
   - Create a new database named `ewaste_quiz`
   - Update the database URL in `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost/ewaste_quiz
```

5. Initialize the database:
```bash
python populate_db.py
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
- `populate_db.py` - Database population script
- `requirements.txt` - Python dependencies

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License. 