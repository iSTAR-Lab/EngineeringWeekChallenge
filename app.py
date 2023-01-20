import os
import uuid
from datetime import datetime
from sqlite3 import connect
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/validate', methods=['POST'])
def validate():
    # Check if password is valid
    password = os.getenv('PASSWORD')
    if request.form['name'] and request.form['password'] == password:
        store_entry_in_database(request.form['name'])
        return render_template('success.html', name=request.form['name'])
    else:
        return render_template('failure.html')


@app.route('/leaderboard')
def leaderboard():
    names = get_entries_from_database()
    if not names:
        names = [{'name': 'No entries yet!', 'time': ''}]
    return render_template('leaderboard.html', names=names)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Check if password is valid
        password = os.getenv('ADMIN_PASSWORD')
        print(request.form['password'])
        if request.form['password'] == password:
            return render_template('admin_panel.html', names=get_entries_from_database())
        else:
            return render_template('admin_login.html')
    else:
        return render_template('admin_login.html')


@app.route('/admin/db_action', methods=['POST'])
def db_action():
    # Get variables from JSON body
    action = request.json['action']
    print(f'Database Action: {action}')
    if action == 'delete':
        delete_entry_from_database(request.json['id'])
    elif action == 'clear':
        clear_database()
    elif action == 'create':
        conn = connect('leaderboard.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS leaderboard (name TEXT, time TEXT)')
        conn.close()
    elif action == 'add':
        store_entry_in_database(request.json['name'])
    return render_template('admin_panel.html', names=get_entries_from_database())


def store_entry_in_database(name: str):
    # Get current datetime
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Store name and time in sqlite database
    conn = connect('leaderboard.db')
    c = conn.cursor()
    # Generate unique ID
    id = str(uuid.uuid4())
    c.execute('INSERT INTO leaderboard VALUES (?, ?, ?)', (id, name, time))
    conn.commit()
    conn.close()


def get_entries_from_database():
    # Get entries from sqlite database
    conn = connect('leaderboard.db')
    c = conn.cursor()
    c.execute('SELECT * FROM leaderboard')
    entries = c.fetchall()
    conn.close()

    # Convert to dictionary
    return_entries = []
    for entry in entries:
        return_entries.append(
            {'id': entry[0], 'name': entry[1], 'time': entry[2]})

    # Sort entries by time
    return_entries.sort(key=lambda x: x['time'])
    return return_entries


def delete_entry_from_database(id: str):
    # Delete entry from sqlite database
    conn = connect('leaderboard.db')
    c = conn.cursor()
    print(f'Deleting {id} from database...')
    c.execute('DELETE FROM leaderboard WHERE id=?', (id,))
    conn.commit()
    conn.close()


def clear_database():
    # Delete all entries from sqlite database
    conn = connect('leaderboard.db')
    c = conn.cursor()
    c.execute('DELETE FROM leaderboard')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    conn = connect('leaderboard.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS leaderboard (id TEXT, name TEXT, time TEXT)')
    conn.close()
    app.run()
