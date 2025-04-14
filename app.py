from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import os
import re
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

# Validation functions
def validate_name(name):
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name.strip()) > 30:
        return False, "Name must not exceed 30 characters"
    
    if not re.match(r'^[a-zA-Z0-9\s\-_\'.]+$', name):
        return False, "Name contains invalid characters"
    
    # Check for obscene words (expand this list as needed)
    obscene_words = [
    'fuck', 'shit', 'ass', 'bitch', 'dick', 'bastard', 'slut', 'whore', 'cunt',
    'piss', 'douche', 'motherfucker', 'fucker', 'asshole', 'cock', 'tit', 'boob',
    'bollocks', 'bugger', 'crap', 'darn', 'damn', 'jackass', 'prick', 'twat',
    'nigger', 'chink', 'spic', 'kike', 'gook', 'tranny', 'fag', 'faggot',
    'rape', 'rapist', 'jerkoff', 'wanker', 'nutjob', 'skank', 'hoe', 'cum',
    'jizz', 'fisting', 'screw', 'ballsack', 'nutsack', 'snatch', 'shithead',
    'titfuck', 'anal', 'rimjob', 'porn', 'sex', 'suck', 'blowjob', 'handjob'
]

    name_lower = name.lower()
    for word in obscene_words:
        if word in name_lower:
            return False, "Name contains inappropriate language"
    
    return True, ""

def validate_score(score):
    try:
        score = int(score)
        if score < 0 or score > 10:
            return False, "Score must be between 0 and 10"
        return True, ""
    except (ValueError, TypeError):
        return False, "Score must be a valid number"

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(IST))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    leaderboard = QuizAttempt.query.order_by(QuizAttempt.score.desc()).limit(4).all()
    return render_template('index.html', leaderboard=leaderboard, is_admin=current_user.is_admin if not current_user.is_anonymous else False)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        player_name = request.form.get('player_name', '').strip()
        is_valid, message = validate_name(player_name)
        if not is_valid:
            flash(message)
            return redirect(url_for('index'))
        return render_template('quiz.html', player_name=player_name, is_admin=current_user.is_admin if not current_user.is_anonymous else False)
    return redirect(url_for('index'))

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    player_name = data.get('player_name', '').strip()
    score = data.get('score')
    
    # Validate inputs
    name_valid, name_message = validate_name(player_name)
    if not name_valid:
        return jsonify({'success': False, 'message': name_message})
    
    score_valid, score_message = validate_score(score)
    if not score_valid:
        return jsonify({'success': False, 'message': score_message})
    
    new_attempt = QuizAttempt(player_name=player_name, score=score)
    db.session.add(new_attempt)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password and user.is_admin:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html', is_admin=current_user.is_admin if not current_user.is_anonymous else False)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    history = QuizAttempt.query.order_by(QuizAttempt.timestamp.desc()).all()
    leaderboard = QuizAttempt.query.order_by(QuizAttempt.score.desc()).limit(4).all()
    return render_template('admin_dashboard.html', history=history, leaderboard=leaderboard, is_admin=True)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

# New Admin CRUD Routes
@app.route('/admin/user/create', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    player_name = data.get('player_name', '').strip()
    score = data.get('score')
    
    # Validate inputs
    name_valid, name_message = validate_name(player_name)
    if not name_valid:
        return jsonify({'success': False, 'message': name_message})
    
    score_valid, score_message = validate_score(score)
    if not score_valid:
        return jsonify({'success': False, 'message': score_message})
    
    new_attempt = QuizAttempt(player_name=player_name, score=score)
    db.session.add(new_attempt)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User created successfully'})

@app.route('/admin/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    attempt = QuizAttempt.query.get_or_404(user_id)
    data = request.get_json()
    
    player_name = data.get('player_name', '').strip()
    score = data.get('score')
    
    # Validate inputs
    name_valid, name_message = validate_name(player_name)
    if not name_valid:
        return jsonify({'success': False, 'message': name_message})
    
    score_valid, score_message = validate_score(score)
    if not score_valid:
        return jsonify({'success': False, 'message': score_message})
    
    attempt.player_name = player_name
    attempt.score = score
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User updated successfully'})

@app.route('/admin/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    attempt = QuizAttempt.query.get_or_404(user_id)
    db.session.delete(attempt)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123', is_admin=True)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True) 