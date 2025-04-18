
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

reminders = []

def check_reminders():
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        for reminder in reminders:
            if reminder['datetime'] == now and not reminder['notified']:
                reminder['notified'] = True
                print(f"Reminder: {reminder['message']}")
        time.sleep(30)

@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

@app.route('/add', methods=['POST'])
def add():
    message = request.form['message']
    date = request.form['date']
    time_ = request.form['time']
    repeat = request.form['repeat']
    datetime_str = f"{date} {time_}"
    reminders.append({
        'message': message,
        'datetime': datetime_str,
        'repeat': repeat,
        'notified': False
    })
    return redirect(url_for('index'))

if __name__ == '__main__':
    threading.Thread(target=check_reminders, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
