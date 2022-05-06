from typing import List

from models.mixpanel import MixpanelReport
from models.report import SectionReports
from utils.format import format_number
from utils.mixpanel import mp_extract

# users
users_reports = [
	MixpanelReport("installazioni avvenute nel periodo (fonte Mixpanel)", 13850641),
	MixpanelReport("login avvenuti con SPID", 13850659),
	MixpanelReport("login avvenuti con CIE", 15507536),
	MixpanelReport("utenti hanno aperto l'app", 13914117),
	MixpanelReport("utenti hanno aperto l'app e sono autenticati", 13850683),
	MixpanelReport(None, 29779677, extractor=
	lambda item: {"android": mp_extract("android/all")(item), "ios": mp_extract("ios/all")(item)},
	               formatter=lambda data: f"- `{format_number(data['android'])}` utenti Android, `{format_number(data['ios'])}` utenti iOS")
]
users_section = SectionReports(":blue-heart-io: *Accesso e Utenti*", users_reports)

# messages
messages_reports = [
	MixpanelReport("messaggi contengono un avviso di pagamento, tra tutti quelli letti dagli utenti",
	               28160628)]
messages_section = SectionReports(":email: *Messaggi*", messages_reports)

# profiles
profiles_reports = [MixpanelReport("richieste di cancellazione del profilo", 26787097),
                    MixpanelReport("richieste di download dei dati del profilo", 26787100), ]
profiles_section = SectionReports(":busts_in_silhouette: *Dati Profilo*", profiles_reports)

# devices
devices_reports = [MixpanelReport("dispositivi che supportano l'autenticazione biometrica", 15212227),
                   MixpanelReport("dispositivi con lock screen impostato (pin, segno, faceId, fingerprint)",
                                  28134364)]
devices_section = SectionReports(":iphone: *Dispositivi*", devices_reports)

# preferences
preferences_reports = [
	MixpanelReport("utenti scelgono la configurazione rapida per i servizi", 15507584),
	MixpanelReport("utenti accettano il tracking su Mixpanel", 13828137, extractor=lambda item: (mp_extract(
		"MIXPANEL_SET_ENABLED - Unique/true/all")(item) /
	                                                                                             mp_extract(
		                                                                                             "MIXPANEL_SET_ENABLED - Unique/$overall/all")(
		                                                                                             item) * 100))]
preferences_section = SectionReports(":gear: *Preferenze*", preferences_reports)

# payments
payments_reports = [MixpanelReport("utenti abbandonano un pagamento allo step finale", 26999381,
                                   extractor=mp_extract("interruzione/all")),
                    MixpanelReport("utenti abbandonano l'inserimento di una carta allo step finale",
                                   13913973),
                    MixpanelReport("verifica pagamento effettuata con successo", 15352169,
                                   extractor=mp_extract("successo/all")),
                    MixpanelReport("attivazione pagamento effettuata con successo", 15352239,
                                   extractor=mp_extract("successo/all")),
                    MixpanelReport("numero di pagamenti effettuati con successo", 13913965,
                                   extractor=mp_extract("pagamento effettuato con successo/$overall/all")),
                    MixpanelReport("percentuale di autorizzazioni 3DS andate a buon fine", 27707760,
                                   extractor=mp_extract("successo/all")),
                    MixpanelReport("pagamenti effettuati con carte", 27302180,
                                   extractor=mp_extract("carta di credito/all")),
                    MixpanelReport("pagamenti effettuati con Paypal", 27302180,
                                   extractor=mp_extract("paypal/all")),
                    # MixpanelReport("pagamenti effettuati con Bancomat Pay", 27302180,
                    #                extractor=mp_extract("bancomat pay/all")),

                    MixpanelReport("percentuale pagamenti conclusi con successo allo step finale usando carte",
                                   29544467,
                                   extractor=mp_extract("carta di credito/all")),
                    MixpanelReport("percentuale pagamenti conclusi con successo allo step finale usando Paypal",
                                   29544467,
                                   extractor=mp_extract("paypal/all")),
                    # MixpanelReport("percentuale pagamenti conclusi con successo allo step finale usando Bancomat Pay",
                    #                29544467,
                    #                extractor=mp_extract("bancomat pay/all")),
                    MixpanelReport("strumenti di pagamento eliminati dal portafoglio", 28033951,
                                   extractor=mp_extract("successo/all"))]
payments_section = SectionReports(":moneybag: *Pagamenti*", payments_reports)

# credit cards
credit_cards_reports = [MixpanelReport("carte aggiunte con successo allo step finale", 13913969),
                        MixpanelReport("carte aggiunte nel wallet", 15272532)]
credit_cards_section = SectionReports(":credit_card: *Carte di debito, credito, prepagate*", credit_cards_reports)

# paypal
paypal_reports = [MixpanelReport("account PayPal aggiunti con successo allo step finale", 27301649),
                  MixpanelReport("account Paypal aggiunti nel wallet nel periodo", 27704365),
                  MixpanelReport("account Paypal aggiunti in totale", 28797355)]
paypal_section = SectionReports(":paypal: *Paypal*", paypal_reports)


# assistance


def assistance_formatter(data):
	categories = data[list(data.keys())[0]]
	total = categories["$overall"]["all"]
	del categories["$overall"]
	# sort categories in DESC order
	sorted_categories = sorted(categories, key=lambda k: categories[k]["all"], reverse=True)
	total_tickets = sum(c['all'] for c in categories.values())
	slack_msg = f"- `{format_number(total_tickets)}` tickets aperti nel periodo"
	msg = []
	for cat in sorted_categories[:6]:
		amount = categories[cat]["all"]
		percentage = format_number((amount / total) * 100.0)
		msg.append(f"{format_number(amount)} ({percentage}) - {cat.replace('_', ' ')}")
	slack_msg += "\n- principali categorie per cui il cittadino richiede assistenza\n```" + "\n".join(msg) + "```"
	return slack_msg


assistance_reports = [MixpanelReport("categoria per cui si richiede assistenza", 29338884, extractor=lambda x: x,
                                     formatter=assistance_formatter)]
assistance_section = SectionReports(":information_desk_person::skin-tone-2: *Assistenza*",
                                    assistance_reports)

# bancomat pay
bpay_reports = [MixpanelReport("Bancomat Pay aggiunti in totale", 29553379),
                MixpanelReport("Bancomat Pay aggiunti nel periodo", 29667527)]
bpay_section = SectionReports(":bpay: *Bancomat Pay*", bpay_reports)

sections: List[SectionReports] = [users_section, messages_section, profiles_section, devices_section,
                                  preferences_section, payments_section,
                                  credit_cards_section, paypal_section, bpay_section, assistance_section]