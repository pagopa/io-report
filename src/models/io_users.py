from models.report import Report
from utils.format import format_number


class IOUsersReport(Report):

	def load_data(self) -> any:
		# don't know how to retrieve this data programmatically, PR welcome :D
		self.data = format_number(15591971)
		return self.data
