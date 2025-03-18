import os, pprint
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from flask import Flask, abort, request
from werkzeug.middleware.proxy_fix import ProxyFix

# Load ENV variables
load_dotenv()

# Flask stuff
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1, x_proto=1)
auth_token = os.getenv("AUTH_TOKEN")

### Slack stuff & generic alert method
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

def slackAlert(channel, blocks, text):
    try:
        response = client.chat_postMessage(
            channel=channel,
            blocks=blocks,
            text=text,
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        abort(500, description=e.response["error"])   



## App route for SMS 'method'
@app.route('/sms', methods=['GET'])
# TODO: Would love some auth bits here
def sms_webhook():

    authToken = request.args.get('auth')   
    fromString = request.args.get('from')
    messageString = request.args.get('message')

    if not authToken:
        abort(400, description="The 'auth' parameter is required.")
    if authToken != auth_token:
        abort(401, description="The 'auth' parameter is incorrect.")
    if not fromString:
        abort(400, description="The 'from' parameter is required.")
    if not messageString:
        abort(400, description="The 'message' parameter is required.")

    # Build message blocks and send to generic alert method
    DIVIDER_BLOCK = {"type": "divider"}
    FROM_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (f"*SMS received on phone line from:* {fromString}"),
        },
    }
    MESSAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (f"{messageString}"),
        },
    }
    blocks = [
        FROM_BLOCK,
        DIVIDER_BLOCK,
        MESSAGE_BLOCK,
    ]
    channel="#Alerts"
    slackAlert(channel, blocks, messageString)

    # Return something to the requestor
    return 'OK'




### App routes

### Add other routes as required for other slack webhooks




## App entry point
if __name__ == '__main__':
    app.run(debug=False, port=5000)


