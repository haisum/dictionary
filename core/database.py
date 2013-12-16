from core import app
import json, random, string
from datetime import datetime
from pymongo import Connection
from pymongo.database import Database


"""
Create database Connection
"""
connection = Connection()
db = Database(connection, app.config["MONGODB_DATABASE"])

class DB(object):
	"""

	"""
	def validate(self, data):
		return True

class MongoDB(DB):
	"""

	"""
	structure = {
		"sample_data" : unicode
	}

	def __init__(self):
		self.db = db
		self.errors = dict()

	__collection__ = 'test'
	
	def insert(self, data, do_validate=True):
		if not do_validate or self.validate(data):
			return self.db[self.__collection__].insert(data)
		else:
			return None
		
	def update(self, query, update, upsert =False, multi = False):
		return self.db[self.__collection__].update(query, update, upsert, multi)

	def findOne(self, query={}, columns=None, limit=0, skip=0, sort="_id"):
		projection = columns
		if columns is not None:
			projection = [{column:1} for column in columns]
		return self.db[self.__collection__].findOne(query, projection).sort(sort).skip(skip).limit(limit)

	def find(self, query={}, columns=None, limit=0, skip=0, sort="_id"):
		projection = columns
		if columns is not None:
			projection = [{column:1} for column in columns]
		return self.db[self.__collection__].find(query, projection).sort(sort).skip(skip).limit(limit)

	def search(self, term, query, limit= 0):
		return self.db.runCommand( "text", { "search": term, "limit": limit, "filter" : query })

	def generate_fixture(self, structure):
		assert isinstance(structure, dict) , "current structure was:" + json.loads(structure)
		item = dict()
		for key,value in structure.iteritems():
			if isinstance(value, dict):
				item[key] = self.generate_fixture(value)
			elif isinstance(value, list):
				if len(value) > 0:
					item[key] = [self.generate_fixture(value[0])]
			elif value == list:
				item[key] = [self.get_random_value(unicode, 5) for x in xrange(0,10)]
			elif value == unicode:
				item[key] = self.get_random_value(unicode, 10)
			elif value == int:
				item[key] = self.get_random_value(int, 4)
			elif value == datetime:
				item[key] = datetime.utcnow().isoformat()
			else:
				item[key] = value
		return item

	def get_random_value(self, type=unicode, size=5):
		chars = string.ascii_lowercase + string.ascii_uppercase + " "
		if type == int:
			chars = string.digits
		return ''.join(random.choice(chars) for x in xrange(0, size))
