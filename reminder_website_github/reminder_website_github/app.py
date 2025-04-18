from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        repeat TEXT
    )""")
    conn.commit()
    conn.close()

@app.route('/add', methods=['POST'])
def add_reminder():
    title = request.form['title']
    date = request.form['date']
    repeat = request.form['repeat']

    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute('INSERT INTO reminders (title, date, repeat) VALUES (?, ?, ?)', (title, date, repeat))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/')
def index():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reminders')
    reminders = c.fetchall()
    conn.close()
    return render_template('reminders.html', reminders=reminders)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0")
