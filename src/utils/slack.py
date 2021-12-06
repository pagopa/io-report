import requests
import os
import json

# retrieve slack token from env variables
slack_web_hook = os.getenv('SLACK_WEB_HOOK_TEST', None)
assert slack_web_hook is not None


def send_slack_message_blocks(blocks):
	try:
		requests.post(url=slack_web_hook, data=json.dumps({"blocks": list(map(get_slack_markdown_message,blocks))}),
		              headers={"Content-type": "application/json"})
	except Exception as e:
		print(f"Got an error: {e.response['error']}")


def get_slack_markdown_message(markdown_test):
	return {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": markdown_test
		}
	}
