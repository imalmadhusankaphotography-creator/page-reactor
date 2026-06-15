from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 1. මෙතනට Graph API Explorer එකෙන් ගත්ත "Page Access Token" එක දාන්න
PAGE_ACCESS_TOKEN = "EAAci11igkXcBRjPWN0QejcoCMzceGbXU9Md49NR7M9LbQYNYlPezPDqsfdUTCcb5hFqicIu4zOIxSNh64ZCS4LKKZBQT59ZApGdzDivZBvK2n9m9lHEGiu60fRkN9plmPsdhp7ZAtlf2Au5OxqGAejZBEwxOIevnG00noquelB27vgZCur9cOZCy9Ahoa2gMaCfRMxJhcQuLjcilE8pIdP8qxWQHFznw9Y51TaqzaDkc"

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
    # 2. මෙතන v19.0 වෙනුවට ඔයාගේ v25.0 එක දැම්මා
    url = f"https://graph.facebook.com/v25.0/{comment_id}/reactions"
    params = {
        'type': 'LOVE',
        'access_token': PAGE_ACCESS_TOKEN
    }
    requests.post(url, params=params)

# 3. Render එකට ගැලපෙන විදිහට Port එක හරියටම මෙතනටයි දාන්න ඕනේ:
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
