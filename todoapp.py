from flask import Flask, render_template, request, redirect, url_for
import re
import pickle
import os

app = Flask(__name__)

# Global list to store To Do items
todo_list = []

SAVE_FILE = 'todo_save.pkl'

# Load saved list on startup if it exists
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, 'rb') as f:
        todo_list = pickle.load(f)


def is_valid_email(email):
    """Validate email using regex from Week 3."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def is_valid_priority(priority):
    return priority in ['Low', 'Medium', 'High']


@app.route('/')
def index():
    error = request.args.get('error', None)
    return render_template('index.html', todo_list=todo_list, error=error)


@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '').strip()

    # Data validation
    if not task:
        return redirect(url_for('index', error='Task cannot be empty.'))
    if not is_valid_email(email):
        return redirect(url_for('index', error='Invalid email address.'))
    if not is_valid_priority(priority):
        return redirect(url_for('index', error='Invalid priority value.'))

    # Add item to list
    todo_list.append({
        'id': len(todo_list),
        'task': task,
        'email': email,
        'priority': priority
    })

    # Fix IDs after append
    for i, item in enumerate(todo_list):
        item['id'] = i

    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
    del todo_list[:]
    # Remove save file if it exists
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save():
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect(url_for('index'))


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    to_remove = next((item for item in todo_list if item['id'] == item_id), None)
    if to_remove:
        todo_list.remove(to_remove)
    # Re-index after deletion
    for i, item in enumerate(todo_list):
        item['id'] = i
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
