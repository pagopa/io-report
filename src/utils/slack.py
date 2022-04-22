import requests
import os
import json

# slack token from env variables
slack_web_hook = os.getenv('SLACK_WEB_HOOK', None)
assert slack_web_hook is not None


def get_slack_markdown_message(markdown_text):
	return {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": markdown_text
		}
	}


def send_slack_message_blocks(blocks):
	try:
		block_slice = 10
		count = 0
		while count <= len(blocks):
			requests.post(url=slack_web_hook, data=json.dumps(
				{"blocks": list(map(get_slack_markdown_message, blocks[count:count + block_slice]))}),
			              headers={"Content-type": "application/json"})
			count += block_slice
	except Exception as e:
		print(f"Got an error: {e.response['error']}")
