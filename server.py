from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "alive"})

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.get_json()
    print("Received command:", data)
    return jsonify({"status": "Command received", "data": data})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT env variable
    app.run(host="0.0.0.0", port=port)
