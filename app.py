from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def index():
    with open('last_ping.dat', 'r') as f:
        lastping = f.readline()
    return f'Last ping was: {lastping}'

@app.route('/time', methods=['GET','POST'])
def set_time():
    if request.method == 'POST':
        lastping = request.form['lastping']
        with open('last_ping.dat', 'w') as f:
            f.write(lastping)
        return lastping
    else:
        with open('last_ping.dat', 'r') as f:
            lastping = f.readline()
        return {'lastping': lastping}