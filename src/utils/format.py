

def format_number(value):
	if isinstance(value, float):
		value = "%.2f" % value
	elif isinstance(value, int):
		value = "{:,}".format(value, grouping=True).replace(',', '.')
	return value
