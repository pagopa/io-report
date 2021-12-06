import abc
from typing import Union


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
		raise NotImplementedError("you should implement 'load_data' method in your subclass!")
