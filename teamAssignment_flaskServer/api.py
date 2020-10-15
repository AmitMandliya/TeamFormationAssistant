# import time
from flask import Flask

app = Flask(__name__)


@app.route('/executeAlgo')
def execute_algo():
    exec(open("algo.py").read())
    # exec(open("algo.py").read())
    return {
        'msg': 'success',
    }
