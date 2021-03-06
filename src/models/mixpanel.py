from typing import Any, Union

from models.report import Report
from utils.format import format_number
from utils.mixpanel import MixpanelDataRetriever, default_extractor


class MixpanelReport(Report):
	"""
	MixpanelReport
	dedicated report for mixpanel
	:param report_id identifies the relative report in Mixpanel
	:type kwargs, could contain
		- extractor: a function that accepts a payload and returns some data
		- formatter: a function that accepts some data and returns a string
	"""

	def __init__(self, description, report_id: int, **kwargs):
		super(MixpanelReport, self).__init__(description)
		self.report_id = report_id
		self.data_extractor = kwargs.get("extractor", default_extractor)
		self.formatter = kwargs.get("formatter", self.slack_formatter)

	def slack_formatter(self, data: Any) -> str:
		return f"- `{format_number(data)}` {self.description}"

	def load_report(self) -> Union[str, None]:
		data = MixpanelDataRetriever.load_mixpanel_report(self)
		if data is None:
			return None
		return self.formatter(data)
