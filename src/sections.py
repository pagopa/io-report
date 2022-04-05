from typing import List
from models.mixpanel import create_mixpanel_reports
from models.report import SectionReports
from utils.mixpanel import mp_extract

# users
users_reports = [{"description": "installazioni avvenute nel periodo (fonte Mixpanel)", "id": 13850641},
				 {"description": "login avvenuti con SPID", "id": 13850659},
				 {"description": "login avvenuti con CIE", "id": 15507536},
				 {"description": "utenti hanno aperto l’app", "id": 13914117},
				 {"description": "utenti hanno aperto l'app e sono autenticati", "id": 13850683}]
users_section = SectionReports(":blue-heart-io: *Accesso e Utenti*", create_mixpanel_reports(users_reports))

# messages
messages_reports = [
	{"description": "messaggi contengono un avviso di pagamento, tra tutti quelli letti dagli utenti",
	 "id": 28160628}]
messages_section = SectionReports(":email: *Messaggi*", create_mixpanel_reports(messages_reports))

# profiles
profiles_reports = [{"description": "richieste di cancellazione del profilo", "id": 26787097},
					{"description": "richieste di download dei dati del profilo", "id": 26787100}, ]
profiles_section = SectionReports(":busts_in_silhouette: *Dati Profilo*", create_mixpanel_reports(profiles_reports))

# devices
devices_reports = [{"description": "dispositivi che supportano l'autenticazione biometrica", "id": 15212227},
				   {"description": "dispositivi con lock screen impostato (pin, segno, faceId, fingerprint)",
					"id": 28134364}, ]
devices_section = SectionReports(":iphone: *Dispositivi*", create_mixpanel_reports(devices_reports))

# preferences
preferences_reports = [
	{"description": "utenti scelgono la configurazione rapida per i servizi", "id": 15507584},
	{"description": "utenti accettano il tracking su Mixpanel", "id": 13828137, "extractor": lambda item: (item[
																													"MIXPANEL_SET_ENABLED - Unique"][
																													"true"][
																													"all"] /
																												item[
																													"MIXPANEL_SET_ENABLED - Unique"][
																													"$overall"][
																													"all"]) * 100}, ]
preferences_section = SectionReports(":gear: *Preferenze*", create_mixpanel_reports(preferences_reports))

# payments
payments_reports = [{"description": "utenti abbandonano un pagamento allo step finale", "id": 26999381,
					 "extractor": mp_extract("interruzione/all")},
					{"description": "utenti abbandonano l'inserimento di una carta di credito allo step finale",
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
credit_cards_reports = [{"description": "carte di credito aggiunte con successo", "id": 13913969},
						{"description": "carte di credito aggiunte nel wallet", "id": 15272532}, ]
credit_cards_section = SectionReports(":credit_card: *Carte di credito*", create_mixpanel_reports(credit_cards_reports))

# paypal
paypal_reports = [{"description": "account PayPal aggiunti con successo allo step finale", "id": 27301649},
				  {"description": "account Paypal aggiunti nel wallet nel periodo", "id": 27704365},
				  {"description": "account Paypal aggiunti in totale", "id": 28797355}, ]
paypal_section = SectionReports(":paypal: *Paypal*", create_mixpanel_reports(paypal_reports))

sections: List[SectionReports] = [users_section, messages_section, profiles_section, devices_section, preferences_section, payments_section,
			credit_cards_section, paypal_section]