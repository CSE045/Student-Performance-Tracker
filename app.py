from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks INTEGER NOT NULL
            )
        ''')
        # Insert sample data if not exists
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM students')
        if cursor.fetchone()[0] == 0:
            sample_students = [
                ('Alice', '10th', 'Math', 85),
                ('Bob', '10th', 'Science', 45),
                ('Charlie', '9th', 'English', 92),
                ('Diana', '9th', 'Computer', 38),
                ('Eve', '10th', 'Social', 78),
                ('Frank', '9th', 'Math', 55),
                ('Grace', '10th', 'Science', 30),
                ('Henry', '9th', 'English', 88),
                ('Ivy', '10th', 'Computer', 65),
                ('Jack', '9th', 'Social', 42)
            ]
            conn.executemany('INSERT INTO students (name, class, subject, marks) VALUES (?, ?, ?, ?)', sample_students)

def classify_performance(marks):
    if marks < 40:
        return 'Needs Improvement'
    elif marks < 70:
        return 'Average'
    else:
        return 'Good'

def get_study_materials(subject):
    materials = {
        'Math': {
            'tip': 'Spend more time practicing problems daily. Focus on understanding formulas instead of memorizing.',
            'links': [
                {'name': 'Khan Academy – Math Practice', 'url': 'https://www.khanacademy.org/math'},
                {'name': 'YouTube: Math Concepts for Beginners', 'url': 'https://www.youtube.com/results?search_query=math+concepts+for+beginners'},
                {'name': 'BYJU’S Math Lessons', 'url': 'https://byjus.com/maths/'}
            ]
        },
        'Science': {
            'tip': 'Revise the core concepts and perform simple home experiments to visualize topics.',
            'links': [
                {'name': 'Khan Academy – Science', 'url': 'https://www.khanacademy.org/science'},
                {'name': 'YouTube: Physics & Chemistry Explained', 'url': 'https://www.youtube.com/results?search_query=physics+chemistry+explained'}
            ]
        },
        'English': {
            'tip': 'Read short stories and newspapers to improve comprehension. Practice writing essays and grammar daily.',
            'links': [
                {'name': 'BBC Learning English', 'url': 'https://www.bbc.co.uk/learningenglish/'},
                {'name': 'Grammarly Blog – English Grammar', 'url': 'https://www.grammarly.com/blog/category/grammar/'},
                {'name': 'YouTube: Spoken English Tips', 'url': 'https://www.youtube.com/results?search_query=spoken+english+tips'}
            ]
        },
        'Computer': {
            'tip': 'Understand the logic behind code. Practice small coding exercises every day.',
            'links': [
                {'name': 'W3Schools – Python/Java Basics', 'url': 'https://www.w3schools.com/python/'},
                {'name': 'GeeksforGeeks – CS Fundamentals', 'url': 'https://www.geeksforgeeks.org/'},
                {'name': 'YouTube: Programming Tutorials', 'url': 'https://www.youtube.com/results?search_query=programming+tutorials'}
            ]
        },
        'Social': {
            'tip': 'Focus on timelines and key events. Create short notes or mind maps for better retention.',
            'links': [
                {'name': 'NCERT Notes (History, Civics, Geography)', 'url': 'https://ncert.nic.in/textbook.php'},
                {'name': 'YouTube: Study IQ Education', 'url': 'https://www.youtube.com/c/StudyIQeducation'},
                {'name': 'BYJU’S Social Studies Lessons', 'url': 'https://byjus.com/social-science/'}
            ]
        }
    }
    return materials.get(subject, {'tip': 'Spend more time studying.', 'links': [{'name': 'General Study Resources', 'url': '#'}]})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/manage')
def manage():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    with get_db() as conn:
        students = conn.execute('SELECT * FROM students').fetchall()
    return render_template('manage.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        class_ = request.form['class']
        subject = request.form['subject']
        marks = int(request.form['marks'])
        with get_db() as conn:
            conn.execute('INSERT INTO students (name, class, subject, marks) VALUES (?, ?, ?, ?)',
                         (name, class_, subject, marks))
        flash('Student added successfully!', 'success')
        return redirect(url_for('manage'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    with get_db() as conn:
        student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        class_ = request.form['class']
        subject = request.form['subject']
        marks = int(request.form['marks'])
        with get_db() as conn:
            conn.execute('UPDATE students SET name = ?, class = ?, subject = ?, marks = ? WHERE id = ?',
                         (name, class_, subject, marks, id))
        flash('Student updated successfully!', 'success')
        return redirect(url_for('manage'))
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    with get_db() as conn:
        conn.execute('DELETE FROM students WHERE id = ?', (id,))
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('manage'))

@app.route('/suggestions/<int:id>')
def suggestions(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    with get_db() as conn:
        student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    performance = classify_performance(student['marks'])
    material_link = get_study_materials(student['subject'])
    return render_template('suggestions.html', student=student, performance=performance, material_link=material_link)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
