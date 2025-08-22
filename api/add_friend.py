from flask import Flask, request, jsonify
import requests
from byte import Encrypt_ID, encrypt_api
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# نحدد عدد الخيوط المتزامنة (50)
executor = ThreadPoolExecutor(max_workers=50)

def send_friend_request(token, uid):
    try:
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
            return {"status": "success", "uid": uid, "message": "Friend request sent!"}
        else:
            return {"status": "failed", "uid": uid, "code": response.status_code, "response": response.text}
    except Exception as e:
        return {"status": "error", "uid": uid, "error": str(e)}

@app.route("/add_friend", methods=["POST"])
def add_friend_batch():
    try:
        body = request.json
        token = body.get("token")
        uids = body.get("uids")  # الآن نستقبل قائمة UIDs

        if not token or not uids:
            return jsonify({"error": "Missing token or uids"}), 400

        futures = [executor.submit(send_friend_request, token, uid) for uid in uids]
        results = [f.result() for f in as_completed(futures)]

        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
