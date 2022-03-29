from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__, instance_relative_config=True)
app = Flask(__name__)

app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Metrics(db.Model):
    __tablename__ = 'Metrics'
    lastping = db.Column(db.DateTime, primary_key=True)
    cpu_usage = db.Column(db.Numeric(4,2))
    ram_usage = db.Column(db.Numeric(4,2))
    disk_usage = db.Column(db.Numeric(4,2))

    def __init__(self, lastping, cpu_usage, ram_usage, disk_usage):
        self.lastping = lastping
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.disk_usage = disk_usage


@app.route('/')
def index():
    with open('last_ping.dat', 'r') as f:
        lastping = f.readline()
    return f'Last ping was: {lastping}'

@app.route('/update', methods=['GET','POST'])
def set_time():
    if request.method == 'POST':
        lastping = request.form['lastping']
        cpu_usage = request.form['cpu-usage']
        ram_usage = request.form['ram-usage']
        disk_usage = request.form['disk-usage']
        row = Metrics(lastping, cpu_usage, ram_usage, disk_usage)
        db.session.add(row)
        db.session.commit()
        #TODO: add better confirmation response
        return "Metrics logged"
    else :
        last_row = Metrics.query.order_by(Metrics.lastping.desc()).first()
        return {
            'lastping': last_row.lastping,
            'cpu_usage': last_row.cpu_usage,
            'ram_usage': last_row.ram_usage,
            'disk_usage': last_row.disk_usage,
        }
