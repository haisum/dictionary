import datetime
from core import app
from core.helpers import route_from

@app.template_global()
def today():
	"""
	returns dictionary of current year, day, month for use in templates
	"""
	today = datetime.date.today()
	return dict(year=today.strftime("%Y"), day=today.strftime("%d"), month=today.strftime("%m") )

@app.template_global()
def reverse_url_map(url, method=None):
	"""
	returns url route for current url
	"""
	route = route_from(url,method)
	return route[0]

@app.template_global()
def url_args(url, method=None):
	"""
	returns url route for current url
	"""
	route = route_from(url,method)
	return route[1]
