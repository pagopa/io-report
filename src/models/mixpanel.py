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


