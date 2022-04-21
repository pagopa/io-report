import abc
from typing import Union, List, Optional


class Report(metaclass=abc.ABCMeta):
    """
    Report
    interface for a report
    :param description describes the report
    """

    def __init__(self, description: str):
        self.report: Optional[str] = None
        self.description: str = description

    @abc.abstractmethod
    def load_report(self) -> Union[str, None]:
        raise NotImplementedError("you should implement 'load_report' method in your class!")


class SectionReports:
    """
        SectionReports
        represents a section of reports with an header as a section description
        :param header describes the section
        :param reports a list of reports
    """

    def __init__(self, header: str, reports=None):
        if reports is None:
            reports = []
        self.header = header
        self.reports = reports

    def add_report(self, report: Report, index: int):
        self.reports.insert(index, report)

    def append_report(self, report: Report):
        self.reports.append(report)

    def extend_reports(self, reports: List[Report]):
        self.reports.extend(reports)
