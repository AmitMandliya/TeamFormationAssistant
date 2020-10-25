import time
from flask import Flask
from TeamAssigner import assignTeam

app = Flask(__name__)

@app.route('/executeAlgo')
def execute_algo():
    exec(open("algo.py").read())
    #exec(open("algo.py").read())
    assignTeam()
    return {
        'msg': 'success',
    }