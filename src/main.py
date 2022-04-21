from sections import sections
from utils.slack import send_slack_message_blocks
import datetime

'''
env variable to setup
MIXPANEL_SERVICE_TOKEN: the token used to authenticate requests to the Mixpanel API
SLACK_WEB_HOOK: webhook used to send the report to Slack dedicated channel 
'''

today = datetime.datetime.now()
week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)
header = f":bar_chart: <https://github.com/pagopa/io-report|IO weekly report> dal *{week_ago.day}/{week_ago.month}* al *{today.day}/{today.month}*"
slack_msgs = []

for idx, section in enumerate(sections):
	if idx > 0:
		slack_msgs.append("")  # empty line divider
	slack_msgs.append(section.header)
	for r in section.reports:
		print(f"requesting data for '{r.description or 'n/a'}'...")
		report = r.load_report()
		slack_msgs.append(report)

if len(slack_msgs):
	send_slack_message_blocks([header])
	send_slack_message_blocks(["\n".join(slack_msgs)])
