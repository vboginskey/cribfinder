from slackclient import SlackClient
import settings

class Slack:
    def __init__(self):
        self.client = SlackClient(settings.SLACK_TOKEN)

    def post(self, content):
        self.client.api_call(
            "chat.postMessage", channel=settings.SLACK_CHANNEL, text=content,
            username='robotface', icon_emoji=':robot_face:')
