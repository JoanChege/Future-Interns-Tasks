from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['todo_app']
tasks_collection = db['tasks']

@app.route('/')
def index():
    tasks = list(tasks_collection.find())
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = {
        'title': request.form['title'],
        'due_date': request.form['due_date'],
        'notes': request.form['notes'],
        'is_complete': False,
        'created_at': datetime.utcnow()
    }
    tasks_collection.insert_one(task)
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

@app.route('/complete/<task_id>')
def complete_task(task_id):
    tasks_collection.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'is_complete': True}}
    )
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
