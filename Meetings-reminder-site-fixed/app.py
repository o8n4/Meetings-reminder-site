from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

reminders = []

def reminder_checker():
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        for r in reminders:
            if r['datetime'] == now and not r.get('notified', False):
                r['notified'] = True
                print(f"Reminder: {r['title']}")
        time.sleep(60)

@app.route('/')
def index():
    return render_template('reminders.html', reminders=reminders)

@app.route('/add', methods=['POST'])
def add_reminder():
    title = request.form['title']
    date = request.form['date']
    time_ = request.form['time']
    dt_str = f"{date} {time_}"
    reminders.append({'title': title, 'datetime': dt_str, 'notified': False})
    return redirect(url_for('index'))

if __name__ == '__main__':
    threading.Thread(target=reminder_checker, daemon=True).start()
    app.run(debug=True)
