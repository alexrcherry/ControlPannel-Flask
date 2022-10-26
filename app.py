from flask import Flask, render_template, request
from datetime import datetime
from flask_sock import Sock
import random
import time
import json


app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/control", methods=['GET', 'POST'])
def control():
    if "open1" in request.form:
        print('open')
    elif "close1" in request.form:
        print('close')

    return render_template('controlPanel.html')


@app.route('/testing/')
def testing():
    return render_template('testingGraph.html')


@app.route('/graph/')
def graph():
    return render_template("graph.html")


@sock.route('/graph/data0')
def graph_data0(sock):
    while True:

        graph_dict = dict()
        graph_dict['label'] = str(datetime.utcnow().strftime("%H:%M:%S"))
        graph_dict['data0'] = random.randint(0, 10)
        graph_dict['data1'] = random.randint(0, 10)
        graph_dict['data2'] = random.randint(0, 10)
        graph_dict['data3'] = random.randint(0, 10)
        data = json.dumps(graph_dict, separators=(',', ':'))
        sock.send(data)
        time.sleep(1)


if __name__ == "__main__":
    app.run(debug=True)
