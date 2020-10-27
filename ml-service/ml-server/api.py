# import time
from flask import Flask
from TeamAssigner import assignTeam

app = Flask(__name__)


@app.route('/executeAlgo')
def execute_algo():
<<<<<<< HEAD
    assignTeam()
=======
    exec(open("algo.py").read())
    # exec(open("algo.py").read())
    assignTeam()	
>>>>>>> e68a90c3a3b38942017cc6d6c42214945cc17a21
    return {
        'msg': 'success',
    }
