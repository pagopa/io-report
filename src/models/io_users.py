from models.report import Report
from utils.format import format_number


class IOUsersReport(Report):

	def load_data(self) -> any:
		# don't know how to retrieve this data programmatically, PR welcome :D
		self.data = format_number(14274335)
		return self.data


class MyAwesomeReport(Report):

	def load_data(self) -> any:
		self.data = format_number(self.my_db_precious_data())
		return self.data

	def my_db_precious_data(self):
		pass
