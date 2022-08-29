from asyncio import tasks
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sock import Sock
import random
import time
import json


app = Flask(__name__)
sock = Sock(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __reper__(self):
        return '<Task %r>' % self.idexit(0)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try: 
           db.session.add(new_task) 
           db.session.commit()
           return redirect('/')
        except: 
           return 'there was an issue returning your task' 
    else:
        task = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=task)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting that task'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating that task'
    else:
        return render_template('update.html',task = task)

        
@app.route('/testing/')
def testing():
    return render_template('testingGraph.html')


@app.route('/graph/')
def graph():
    return render_template("graph.html")
@sock.route('/graph/data')
def graph_data(sock):
    while True:
        
        graph_dict = dict()
        graph_dict['label'] = str(datetime.utcnow().strftime("%H:%M:%S"))
        graph_dict['data'] = random.randint(0,10)
        data = json.dumps(graph_dict, separators=(',', ':'))
        sock.send(data)
        time.sleep(1)

@app.route('/echo')
def echo_index():
    return render_template('echo.html')

@sock.route('/echo/test')
def echo(sock):
    i = 0
    while True:
        #data = sock.receive()
        sock.send(str(random.randint(0,10)))
        i += 1
        time.sleep(1)

if __name__ == "__main__":
    app.run(debug=True)