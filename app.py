from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAci11igkXcBRjaLPgz3iMdohFG3hss7gofQDYZAQC1xK0jVRpZAuodfVqxgjciTnXZAeNpvx3g3okkAp3GhxnEm9QdiHwIqECtaU05GqZBURugWmJ7JLoQfPEa9X62XR2inF10akmBQSOkFv3qulqQzM6UVB5blxpZAHbZBuLltF0DJ2C1oesJAJCnVieZBKXLiqh11XIRqvvjR777eGzr7V7LmXHnZBAK7LQFxLY2Ph2IDkwzBzHZCMRZA7uIfH2bYNVlRFtu6eEny0ZD"

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
