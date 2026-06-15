from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAci11igkXcBRiaz2BZCkhc0j5WKTyb80r0wU6KF6WEWaZAtA3ME1YMceu6ugbtytO8RyFXO8CNxMgZCbgeNH0BZBPVm1cD1zGbGN55DKE1u6dCE2ngtVkAZB2N8Mc0ZCKKB51NtDrBfto9RHlNIeJ2DbdHC9ZAUtVEZAQ6ZBeJpv1lKhXwKR8bV6huBC52dKMF2UcfZBUyzrr89n5D9luOl95EorRDVuUXsKts21P4FIZD"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == 'mytoken123':
        return request.args.get('hub.challenge')
    return 'Error', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    for entry in data.get('entry', []):
        for change in entry.get('changes', []):
            if change['field'] == 'feed':
                item = change['value']
                if item.get('item') == 'comment':
                    comment_id = item['comment_id']
                    react(comment_id)
    return 'OK', 200

def react(comment_id):
    url = f"https://graph.facebook.com/v19.0/{comment_id}/reactions"
    params = {
        'type': 'LOVE',
        'access_token': PAGE_ACCESS_TOKEN
    }
    requests.post(url, params=params)

if __name__ == '__main__':
    app.run()
