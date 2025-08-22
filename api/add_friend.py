from flask import Flask, request, jsonify
import requests
from byte import Encrypt_ID, encrypt_api
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# نسمح بـ 50 طلب متزامن
executor = ThreadPoolExecutor(max_workers=50)

def send_request(token, uid):
    uid = int(uid)
    id_encrypted = Encrypt_ID(uid)
    data0 = "08c8b5cfea1810" + id_encrypted + "18012008"
    data = bytes.fromhex(encrypt_api(data0))

    url = "https://clientbp.common.ggbluefox.com/RequestAddingFriend"
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'Authorization': f'Bearer {token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB50',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return {"status": "success", "message": "Friend request sent!"}
    else:
        return {"status": "failed", "code": response.status_code, "response": response.text}

@app.route("/add_friend", methods=["GET"])
def add_friend():
    token = request.args.get("token")
    uid = request.args.get("uid")

    if not token or not uid:
        return jsonify({"error": "Missing token or uid"}), 400

    # تنفيذ الطلب في خيط مستقل
    future = executor.submit(send_request, token, uid)
    result = future.result()

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
