from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)

# Ensure database tables are created
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_date = request.args.get('date', datetime.today().strftime("%Y-%m-%d"))
    students = Attendance.query.filter_by(date=selected_date).all()
    return render_template('index.html', students=students, selected_date=selected_date)

@app.route('/add_student', methods=['POST'])
def add_student():
    roll_no = request.form.get('roll_no')
    name = request.form.get('name')
    status = request.form.get('status')  # Get "Present" or "Absent" from form
    date = datetime.today().strftime("%Y-%m-%d")

    # Check if student already exists for the selected date
    existing_student = Attendance.query.filter_by(roll_no=roll_no, date=date).first()
    if not existing_student:
        new_student = Attendance(roll_no=roll_no, name=name, date=date, status=status)
        db.session.add(new_student)
        db.session.commit()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
