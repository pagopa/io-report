import requests
import os
from typing import Callable, Union, Optional
from models.report import Report
from utils.format import format_number


def default_extractor(series):
	first_key = list(series.keys())[0]
	return series[first_key]["all"]


class MixpanelReport(Report):
	"""
	MixpanelReport
	dedicated report for mixpanel
	:param report_id identifies the relative report in Mixpanel
	:param data_extractor extracts the data in a specific position in the mixpanel payload
	:type report_id: int
	:type data_extractor: Callable
	"""

	def __init__(self, description, report_id: int, data_extractor: Union[
		Optional[Callable]] = default_extractor):
		super(MixpanelReport, self).__init__(description)
		self.report_id = report_id
		self.mixpanel_data_retriever = MixpanelDataRetriever()
		self.data_extractor = default_extractor if data_extractor is None else data_extractor

	def load_data(self) -> any:
		self.data = self.mixpanel_data_retriever.load_mixpanel_report(self)
		if self.data:
			self.data = format_number(self.data)
		return self.data


class MixpanelDataRetriever:
	project_id = 2460815
	# see https://eu.mixpanel.com/report/2460815/settings/#project/2460815/serviceaccounts
	mixpanel_token = os.getenv('MIXPANEL_SERVICE_TOKEN', None)
	assert mixpanel_token is not None

	url = f"https://eu.mixpanel.com/api/2.0/insights?project_id={project_id}"
	headers = {
		"Accept": "application/json",
		"Authorization": f"Basic {mixpanel_token}"
	}

	def load_mixpanel_report(self, report: MixpanelReport):
		try:
			response = requests.request("GET", MixpanelDataRetriever.url + f"&bookmark_id={report.report_id}",
			                            headers=MixpanelDataRetriever.headers)
			data = response.json()
			series = data["series"]
			return report.data_extractor(series)
		except:  # todo handle timeout & retries
			import traceback
			traceback.print_exc()
			return None


# see https://docs.google.com/spreadsheets/d/11sJKhW5BPdg5GnttZc78oWKk0jMBkKCSgRnG5sgfCwQ/edit#gid=0
_mixpanel_reports = [
	{"description": "# download nel periodo (fonte mixpanel)", "id": 13850641},
	{"description": "% login successo con SPID", "id": 13850659},
	{"description": "% login successo con CIE", "id": 15507536},
	{"description": "# utenti attivi", "id": 13914117},
	{"description": "# utenti attivi (loggati)", "id": 13850683},
	{"description": "# richieste di cancellazione del profilo", "id": 26787097},
	{"description": "# richieste di download dei dati del profilo", "id": 26787100},
	{"description": "% di dispositivi con autenticazione biometrica", "id": 15212227},
	{"description": "% verifica pagamento effettuata con successo", "id": 15352169,
	 "extractor": lambda item: item["successo"]["all"]},
	{"description": "% attivazione pagamento effettuata con successo", "id": 15352239,
	 "extractor": lambda item: item["successo"]["all"]},
	{"description": "# pagamenti effettuati con successo", "id": 27163336},
	{"description": "% pagamenti effettuati con successo", "id": 26999327,
	 "extractor": lambda item: item["successo"]["all"]},
	{"description": "% utenti che abbandonano l'inserimento di un pagamento durante il checkout", "id": 26999381,
	 "extractor": lambda item: item["interruzione"]["all"]},
	{"description": "% utenti che abbandonano l'inserimento di una carta di credito durante il checkout",
	 "id": 13913973},
	{"description": "% carte di credito aggiunte con successo", "id": 13913969},
	{"description": "# carte di credito aggiunte nel wallet", "id": 15272532},
	{"description": "% preferenze servizi - auto", "id": 15507584},
	{"description": "% condivide i dati con Mixpanel", "id": 13828137, "extractor": lambda item: (item[
		                                                                                              "MIXPANEL_SET_ENABLED - Unique"][
		                                                                                              "true"]["all"] /
	                                                                                              item[
		                                                                                              "MIXPANEL_SET_ENABLED - Unique"][
		                                                                                              "$overall"][
		                                                                                              "all"]) * 100},
]

mixpanel_reports = []
for r in _mixpanel_reports:
	report = MixpanelReport(r["description"], r["id"], r.get("extractor", None))
	mixpanel_reports.append(report)
