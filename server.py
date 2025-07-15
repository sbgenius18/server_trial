from flask import Flask, jsonify, request
import time
import yagmail
EMAIL_USER = "familyphotosparity002@gmail.com"
EMAIL_PASS = "vsmm hbqg romf phiz"
SEND_TO = "shreyasbkg1@gmail.com"
yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
app = Flask(__name__)
device_names = []
device_timeStamps = []
task_arr = []
file_path = []


@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    print("Received data from client:", data)
    return jsonify({"status": "received", "data": data})


#used by client to log username and time
@app.route('/get_username', methods=['POST'])
def get_username():
    global device_names
    global task_arr 
    global file_path 
    data = request.get_json()
    print(f"Username received: {data['username']}")
    print(f"Before append, device_names: {device_names}")
    if data["username"] not in device_names:
        device_names.append(data["username"])
        device_timeStamps.append(data["timeStamp"])
        task_arr.append("idle")
        file_path.append("null")
    device_timeStamps[device_names.index(data["username"])] = data["timeStamp"]
    print(device_names)
    print(device_timeStamps)
    return jsonify({"status": "USername Sent","task":task_arr[device_names.index(data["username"])],"path":file_path[device_names.index(data["username"])]})




    
    

#used by controller
@app.route('/get_online_details', methods=['POST'])
def get_online_details():
    arr = []
    global device_names
    global device_timeStamps
    for i in range(len(device_names)):
        if time.time()-device_timeStamps[i] <= 120:
            arr.append(device_names[i])
            try:
                body = "\n".join(device_names)
                yag.send(SEND_TO, "online details current",body)
                return jsonify({"status": "List sent","task":"idle"})
            except Exception as e:
                print(f"Error sending email: {e}")
                return jsonify({"status": "Error sending list"})
        else:
            return jsonify({"status": "Nobody Online"})
    

#method for controller to set path for viewing    
@app.route('/read_dir', methods=['POST'])
def read_dir():
    data = request.get_json()
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
    


if __name__ == '__main__':
    app.run(debug=True)
