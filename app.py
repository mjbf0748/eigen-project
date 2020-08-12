from flask import Flask, jsonify, request 
from flask_cors import CORS 
import sys
sys.path.insert(1, './routes') # point to routes folder
import werkzeug._internal

import router

app = Flask(__name__)
cors = CORS(app, resources={r"/api": {"origins": "*"}})

def demi_logger(type, message, *args, **kwargs):
    pass

# Route to find important words
@app.route("/api", methods=['POST'])
def findWords():
    files = request.files
    res = router.extractWords(files)
    return jsonify(res)

if __name__ == '__main__':
    werkzeug._internal._log = demi_logger
    app.run(host='0.0.0.0', debug=True)
