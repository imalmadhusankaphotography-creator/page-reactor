from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAci11igkXcBRkCOWRMG3YItZCLEcHbP7ekn9lTdu0eU6sKguMi57W1YZByKbGc0dbNycCcpH0B5ZCahZAQUMQ7yw5UPPbRBL0LcZAxDaTlPTDhYrgKOsZBArtaNs486gZBxytV6fpMSJYCdOnSEcNLZC1p4Az93iJimhVc5ZAdVMLmzsZA3IMfnmSm5avx3eIbZA9QwyKP0ZBOLdMA93oZBnFonEOD6Ci8QKnFJm0OvJN78ewwft1LSxPnSlfWfAlUMdjdVtkCTfixf7duIZD"

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
