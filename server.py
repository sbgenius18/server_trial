from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "alive"})

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.get_json()
    print("Received command:", data)
    # Here you can log, parse, or forward commands via email API if needed
    return jsonify({"status": "Command received", "data": data})

if __name__ == '__main__':
    app.run()
