from core.database import MongoDB

class User(MongoDB):
	"""
	User model for manipulating users collection
	structure = {
		"nick" : unicode,
		"fullname" : "",
		"email" : "",
		"favourites" : [],
		"roles" : [],
		"reputation" : int,
		"logins" : [{
			'ip' : unicode,
			'date_loggedin' : datetime,
		}],
		"about" : unicode,
		"timezone" : unicode
 	}
	"""
	__collection__ = 'users'