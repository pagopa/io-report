import abc
from typing import Union, List


class Report(metaclass=abc.ABCMeta):
	"""
	Report
	interface for a report
	:param description describes the report
	"""

	def __init__(self, description: str):
		self.data: Union[float, int, str, None] = None
		self.description: str = description

	@abc.abstractmethod
	def load_data(self) -> Union[float, int, str, None]:
		raise NotImplementedError("you should implement 'load_data' method in your class!")


class SectionReports:
	"""
		SectionReports
		represents a sections of reports with an header as a section description
		:param header describes the section
		:param reports a list of reports
	"""

	def __init__(self, header: str, reports: List[Report] = []):
		self.header = header
		self.reports = reports

	def add_report(self, report: Report, index: int):
		self.reports.insert(index, report)

	def append_report(self, report: Report):
		self.reports.append(report)

	def extend_reports(self, reports: List[Report]):
		self.reports.extend(reports)
