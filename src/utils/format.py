import locale


def format_number(value):
	locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
	if isinstance(value, float):
		value = locale.format_string("%0.2f", value) + '%'
	elif isinstance(value, int):
		value = "{:,}".format(value, grouping=True).replace(',', '.')
	return value
