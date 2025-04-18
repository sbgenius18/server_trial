from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')

    if num1 is None or num2 is None:
        return jsonify({"error": "Missing inputs"}), 400

    result = num1 + num2
    return jsonify({"result": result})


@app.route('/sub', methods=['POST'])
def sub_numbers():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')

    if num1 is None or num2 is None:
        return jsonify({"error": "Missing inputs"}), 400

    result = num1 - num2
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)