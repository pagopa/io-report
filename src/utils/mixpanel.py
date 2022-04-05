import os
import requests
from time import sleep

from models.report import Report


def mp_extract(path):
	resources = path.split("/")

	def extract(item):
		for r in resources:
			item = item[r]
		return item

	return extract


def default_extractor(series):
	first_key = list(series.keys())[0]
	return series[first_key]["all"]


class MixpanelDataRetriever:
	# seconds to sleep before make another attempt to try to retrieve data
	retry_delay = 2.0
	# max attempts when a request fail. After that the request is considered failed
	max_attempts = 3
	project_id = 2460815
	# see https://eu.mixpanel.com/report/2460815/settings/#project/2460815/serviceaccounts
	mixpanel_token = os.getenv('MIXPANEL_SERVICE_TOKEN', None)
	assert mixpanel_token is not None

	url = f"https://eu.mixpanel.com/api/2.0/insights?project_id={project_id}"
	headers = {
		"Accept": "application/json",
		"Authorization": f"Basic {mixpanel_token}"
	}

	@staticmethod
	def load_mixpanel_report(mixpanel_report: Report):
		attempts = 0
		while attempts < MixpanelDataRetriever.max_attempts:
			attempts += 1
			try:
				response = requests.request("GET",
											MixpanelDataRetriever.url + f"&bookmark_id={mixpanel_report.report_id}",
											headers=MixpanelDataRetriever.headers)
				print(response.status_code)
				data = response.json()
				series = data["series"]
				value = mixpanel_report.data_extractor(series)
				return value
			except:
				import traceback
				traceback.print_exc()
				sleep(MixpanelDataRetriever.retry_delay)
		print(f"cant load mixpanel report '{mixpanel_report.description}'")
		return None

