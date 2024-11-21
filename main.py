from flask import Flask, render_template, session, redirect, url_for, request
import sqlite3
from markupsafe import escape

exercises_dict = {
    'Bench Press': ['Chest', 'Triceps', 'Shoulders'],
    'Squat': ['Legs', 'Glutes', 'Lower Back'],
    'Deadlift': ['Back', 'Legs', 'Forearms'],
    'Bicep Curl': ['Biceps'],
    'Shoulder Press': ['Shoulders', 'Triceps'],
    'Pull-Up': ['Back', 'Biceps'],
    'Lunge': ['Legs', 'Glutes'],
    'Plank': ['Core'],
    'Tricep Extension': ['Triceps'],
    'Leg Press': ['Legs']
}


app = Flask(__name__)
@app.route('/workout')
def workout():
    
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
   
        print("shs")
    return render_template('workout.html')
    

@app.route('/create-workout', methods=['GET','POST'])
def create_workout():
    
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
   
        print("shs")
    return render_template('workout.html')
    


@app.route('/')
def home():
   
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/login')
def login():
  
    return render_template('index.html')

@app.route('/signup')
def signup():

    return render_template('signup.html')

def create():
   
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                Username TEXT PRIMARY KEY,
                Password TEXT
                UserID INTEGER 
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                exercise TEXT,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES Users (Username)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WorkoutSessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES Users (Username)
            )
                       
        """)
        db.commit()
    print('Database table created.')

create()  

@app.route('/insert')
def insert():
    # Insert a test user into the Users table
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Users (Username, Password) VALUES ('Bob', '123')")
        db.commit()
    return 'Test user Bob inserted.'

@app.route('/select')
def select():
    
    try:
        with sqlite3.connect('login.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Users")
            result = cursor.fetchall()
            if len(result) == 0:
                return 'No records found.'
            else:
                return ', '.join(map(str, result))
    except Exception as e:
        return str(e)





@app.route('/add', methods=['POST'])
def add():
    
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)",
                       (request.form['username'], request.form['password']))
        db.commit()
    return request.form['username'] + ' added successfully.'

@app.route('/verify', methods=['POST'])
def verify():
   
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
                       (request.form['username'], request.form['password']))
        result = cursor.fetchall()
        if len(result) == 0:
            return 'Username or password not recognized.'
        else:
            session.permanent = True
            session['username'] = request.form['username']
            return redirect(url_for('home'))  

@app.route('/table')
def table():
    
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users")
        rows = cursor.fetchall()
    return render_template('table.html', rows=rows)

@app.route('/un')
def un():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in.'

@app.route('/logout')
def logout():
    
    session.pop('username', None)
    return redirect(url_for('login'))  


app.secret_key = 'the random string'
app.run(port=5021, debug=True)
