from typing import Callable, Union, Optional, List
from models.report import Report, SectionReports
from utils.format import format_number
from utils.mixpanel import MixpanelDataRetriever, mp_extract, default_extractor


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


def create_mixpanel_reports(reports):
	return list(map(lambda item: MixpanelReport(item["description"], item["id"], item.get("extractor", None)), reports))


# users
users_reports = [{"description": "installazioni avvenute nel periodo (fonte Mixpanel)", "id": 13850641},
				 {"description": "login avvenuti con SPID", "id": 13850659},
				 {"description": "login avvenuti con CIE", "id": 15507536},
				 {"description": "utenti che hanno aperto l’app", "id": 13914117},
				 {"description": "utenti che hanno aperto l'app e sono autenticati:", "id": 13850683}]
users_section = SectionReports(":blue-heart-io: *Accesso e Utenti*", create_mixpanel_reports(users_reports))

# messages
messages_reports = [
	{"description": "di messaggi contenenti un avviso di pagamento, tra tutti quelli letti dagli utenti",
	 "id": 28160628}]
messages_section = SectionReports(":email: *Messaggi*", create_mixpanel_reports(messages_reports))

# profiles
profiles_reports = [{"description": "richieste di cancellazione del profilo", "id": 26787097},
					{"description": "richieste di download dei dati del profilo", "id": 26787100}, ]
profiles_section = SectionReports(":busts_in_silhouette: *Dati Profilo*", create_mixpanel_reports(profiles_reports))

# devices
devices_reports = [{"description": "di dispositivi che supportano l'autenticazione biometrica", "id": 15212227},
				   {"description": "di dispositivi con lock screen impostato (pin, segno, faceId, fingerprint)",
					"id": 28134364}, ]
devices_section = SectionReports(":iphone: *Dispositivi*", create_mixpanel_reports(devices_reports))

# preferences
preferences_reports = [
	{"description": "di utenti che sceglie la configurazione rapida per i servizi", "id": 15507584},
	{"description": "utenti che accettano il tracking su Mixpanel", "id": 13828137, "extractor": lambda item: (item[
																													"MIXPANEL_SET_ENABLED - Unique"][
																													"true"][
																													"all"] /
																												item[
																													"MIXPANEL_SET_ENABLED - Unique"][
																													"$overall"][
																													"all"]) * 100}, ]
preferences_section = SectionReports(":gear: *Preferenze*", create_mixpanel_reports(preferences_reports))

# payments
payments_reports = [{"description": "utenti che abbandonano un pagamento allo step finale", "id": 26999381,
					 "extractor": mp_extract("interruzione/all")},
					{"description": "utenti che abbandonano l'inserimento di una carta di credito allo step finale",
					 "id": 13913973},
					{"description": "verifica pagamento effettuata con successo", "id": 15352169,
					 "extractor": mp_extract("successo/all")},
					{"description": "attivazione pagamento effettuata con successo", "id": 15352239,
					 "extractor": mp_extract("successo/all")},
					{"description": "pagamenti effettuati con successo", "id": 13913965,
					 "extractor": mp_extract("pagamento effettuato con successo/$overall/all")},
					{"description": "pagamenti effettuati con successo", "id": 27707760,
					 "extractor": mp_extract("successo/all")},
					{"description": "pagamenti effettuati con carta di credito", "id": 27302180,
					 "extractor": mp_extract("carta di credito/all")},
					{"description": "pagamenti effettuati con Paypal", "id": 27302180,
					 "extractor": mp_extract("paypal/all")},
					{"description": "strumenti di pagamento eliminati dal portafoglio", "id": 28033951,
					 "extractor": mp_extract("successo/all")}, ]
payments_section = SectionReports(":moneybag: *Pagamenti*", create_mixpanel_reports(payments_reports))

# credit cards
credit_cards_reports = [{"description": "% carte di credito aggiunte", "id": 13913969},
						{"description": "carte di credito aggiunte nel wallet", "id": 15272532}, ]
credit_cards_section = SectionReports(":credit_card: *Carte di credito*", create_mixpanel_reports(credit_cards_reports))

# paypal
paypal_reports = [{"description": "di account PayPal aggiunti con successo allo step finale", "id": 27301649},
				  {"description": "account Paypal aggiunti nel wallet nel periodo", "id": 27704365},
				  {"description": "account Paypal aggiunti in totale", "id": 28797355}, ]
paypal_section = SectionReports(":paypal: *Paypal*", create_mixpanel_reports(paypal_reports))

sections: List[SectionReports] = [users_section, messages_section, profiles_section, devices_section, preferences_section, payments_section,
			credit_cards_section, paypal_section]
