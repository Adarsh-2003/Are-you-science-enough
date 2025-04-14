# How Good is Your Science? - Quiz App

A web-based science quiz application built with Flask, SQLite, and modern web technologies.

## Features

- Interactive 10-question science quiz
- Dynamic leaderboard showing top 4 scorers
- Admin dashboard with quiz history
- Responsive design for all devices
- No login required for taking the quiz
- Secure admin access

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd quiz-app
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Admin Access

Default admin credentials:
- Username: admin
- Password: admin123

**Important:** Change these credentials in production!

## Project Structure

```
quiz-app/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── quiz.html
    ├── admin_login.html
    └── admin_dashboard.html
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 