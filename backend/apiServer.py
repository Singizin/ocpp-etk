from flask import Flask, request, Response, jsonify

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def hello_world():
    input_json = request.get_json(force=True)
    print(request.headers, input_json)
    return jsonify({'Hello World': 123})


@app.route('/api', methods=['GET'])
def hello_world2():
    return jsonify({'Hello World': 123})


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(port=4567)
