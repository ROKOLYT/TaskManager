import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

connection = sqlite3.connect('tasks.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT
    )""")

connection.commit()
connection.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')

        cursor.execute("""UPDATE tasks SET title=?, description=?, status=? WHERE id=?""", (title, description, status, id))
        connection.commit()
        connection.close()
 
        return redirect('/')

    else:
        cursor.execute("""SELECT * FROM tasks WHERE NOT status='Done'""")
        tasks = cursor.fetchall()
        connection.close()
        return render_template('index.html', tasks=tasks)
    
    
@app.route('/add', methods=['POST'])
def add():
    
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    title = request.form.get('title')
    description = request.form.get('description')
    status = request.form.get('status')

    cursor.execute("""INSERT INTO tasks(title, description, status) VALUES(?, ?, ?)""", (title, description, status))
    connection.commit()
    connection.close()

    return redirect('/')

@app.route('/done', methods=['POST'])
def done():
    
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    id = request.form.get('id')

    cursor.execute("""UPDATE tasks SET status='Done' WHERE id=?""", (id))
    connection.commit()
    connection.close()

    return redirect('/')

@app.route('/archive')
def archive():
    
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM tasks WHERE status='Done'""")
    tasks = cursor.fetchall()
    connection.close()
    
    return render_template('archive.html', tasks=tasks)