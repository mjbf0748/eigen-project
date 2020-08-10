from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.insert(1, './routes')

import router
app = Flask(__name__)
cors = CORS(app, resources={r"/api": {"origins": "*"}})

@app.route("/api", methods=['POST'])
def home():
    files = request.files
    # text = myfile.read().decode()
    # print(text)
    res = router.extractWords(files)
    # request.args.get() or .args[] which will said bad request For query params
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
