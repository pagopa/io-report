from models.io_users import IOUsersReport
from models.mixpanel import mixpanel_reports
from utils.slack import send_slack_message_blocks
import datetime

'''
env variable to setup
MIXPANEL_SERVICE_TOKEN: the token used to authenticate requests to the Mixpanel API
SLACK_WEB_HOOK: webhook used to send the report to Slack dedicated channel 
'''

today = datetime.datetime.now()
week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
header = f":bar_chart: <https://docs.google.com/spreadsheets/d/11sJKhW5BPdg5GnttZc78oWKk0jMBkKCSgRnG5sgfCwQ/edit#gid=0|IO weekly stats> dal *{week_ago.day}/{week_ago.month}* al *{today.day}/{today.month}*"
slack_msgs = []

# io user report
reports = [IOUsersReport("# utenti unici")]
# mixpanel report
reports.extend(mixpanel_reports)

for r in reports:
	r.load_data()
	if r.data is None:
		raise IOError(f"cannot retrieve data for report '{r.description}'")
	slack_msgs.append(f"- _{r.description}_: `{r.data}`")

if len(slack_msgs):
	send_slack_message_blocks([header, "\n".join(slack_msgs)])
