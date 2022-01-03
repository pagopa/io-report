from typing import Callable, Union, Optional
from models.report import Report
from utils.format import format_number
from utils.mixpanel import MixpanelDataRetriever


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
		self.data_extractor = default_extractor if data_extractor is None else data_extractor

	def load_data(self):
		self.data = MixpanelDataRetriever.load_mixpanel_report(self)
		if self.data:
			self.data = format_number(self.data)
		return self.data


# see https://docs.google.com/spreadsheets/d/11sJKhW5BPdg5GnttZc78oWKk0jMBkKCSgRnG5sgfCwQ/edit#gid=0
_mixpanel_reports = [
	{"description": "# installazioni nel periodo (fonte Mixpanel)", "id": 13850641},
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
	{"description": "% sceglie la preferenza AUTOMATICA per i servizi", "id": 15507584},
	{"description": "% che condivide i dati con Mixpanel", "id": 13828137, "extractor": lambda item: (item[
																										  "MIXPANEL_SET_ENABLED - Unique"][
																										  "true"][
																										  "all"] /
																									  item[
																										  "MIXPANEL_SET_ENABLED - Unique"][
																										  "$overall"][
																										  "all"]) * 100},
	{"description": "# account Paypal aggiunti", "id": 27301649,
	 "extractor": lambda item: item["successo"]["$overall"]["all"]},
	{"description": "% successo nell'aggiunta di un account Paypal", "id": 27301649,
	 "extractor": lambda item: (item["successo"]["$overall"]["all"] / (
			 (item["fallimento"]["$overall"]["all"] if 'fallimento' in item else 0) + item["successo"]["$overall"][
		 "all"])) * 100},
	{"description": "# pagamenti effettuati con carta di credito", "id": 27302180,
	 "extractor": lambda item: item["carta di credito"].get("0", {"all": 0})[
		 "all"] if "carta di credito" in item else 0},
	{"description": "# pagamenti effettuati con Paypal", "id": 27302180,
	 "extractor": lambda item: item["paypal"]["$overall"].get("0", {"all": 0})["all"] if "paypal" in item else 0},
]

mixpanel_reports = []
for r in _mixpanel_reports:
	report = MixpanelReport(r["description"], r["id"], r.get("extractor", None))
	mixpanel_reports.append(report)
