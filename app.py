import slack
from slack import WebClient
import os
from flask import Flask
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNIN_SECRET'], '/slack/events', app)
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

client.chat_postMessage(channel='#ditto-testing', text='Ditto running...')
BOT_ID = client.api_call("auth.text")

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if user_id != BOT_ID:
        client.chat_postMessage(channel=channel_id, text=text)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
