from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def index():
    with open('last_ping.dat', 'r') as f:
        lastping = f.readline()
    return f'<h1>Last ping was: {lastping}</h1>'

@app.route('/time', methods=['POST'])
def set_time():
    lastping = request.form['lastping']
    with open('last_ping.dat', 'w') as f:
        f.write(lastping)
    return lastping