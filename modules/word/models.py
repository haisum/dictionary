from core import babel,app
from core.database import MongoDB
from bson.objectid import ObjectId
from datetime import datetime
import random, json
from flask.ext.babel import gettext

class Word(MongoDB):
	"""
	Word model for manipulating words collection
	"""

	__collection__ = 'words'

	STATUS = {
		"approved" : 1,
		"pending" : 0,
		"rejected" : -1,
	}

	structure = {
		'language': unicode,
		'local': unicode,
		'phrase' : unicode,
		'translation': unicode,
		'description' : unicode,
		'example' : {
			'local' : unicode,
			'phrase' : unicode,
			'translation' : unicode,
		},
		'tags' : list,
		'likes' : [{
			'user_id' : unicode,
			'date_liked' : datetime,
		}],
		'dislikes' : [{
			'user_id' : unicode,
			'date_disliked' : datetime,
		}],
		'likes_count' : int,
		'dislikes_count' : int,
		'views' : [{
			'user_id' : unicode,
			'date_viewed' : datetime,
		}],
		'views_count' : 1,
		'date_added' : datetime,
		'status' : STATUS["approved"],
		'user_id' : unicode,
		'user_nick' : unicode,
		'random' : unicode
	}

	def __init__(self, user_id, *args, **kwargs):
		self.user_id = user_id
		"""
		Don't delete following line
		"""
		super(self.__class__, self).__init__(*args, **kwargs)


	def insert_word(self, data, do_validate=True):
		data["language"] = data["language"].lower()
		language = Language()
		language.upsert(data["language"])
		data["phrase"] = data["phrase"].lower()
		return self.insert(data, do_validate)

	def validate(self, data):
		"""
		Override base class validate method
		"""
		self.errors = dict()
		status_values = self.STATUS.values()
		if not data["phrase"]:
			self.errors["phrase"] = gettext("Slang is required.")
			if data["language"].lower() != "english":
				self.errors["phrase"] = gettext("When inserting in languages other than English, English pronunciation is required.")
		if len(data["local"]) > 500:
			self.errors["local"] = gettext("Local word too long. Max limit: 500 charachters")
		if data["status"] not in status_values:
			self.errors["status"] = gettext("Invalid status. Should be one of 1(approved), 0(pending) and -1(rejected)")
		if not data["definition"]:
			self.errors["definition"] = gettext("Definition is required while inserting a new word.")
		elif len(data["definition"]) > 500:
			self.errors["definition"] = gettext("Definition too long")
		elif len(data["definition"]) < 5:
			self.errors["definition"] = gettext("Definition too short")
		if "user_id" not in data or data["status"] not in status_values:
			self.errors["user_id"] = gettext("Cookies are disabled. Word can't be added without enabling cookies.")
		if len(data["example"]) > 1000:
			self.errors["example"] = gettext("Example too long. Max limit: 1000 charachters")
		if len(data["tags"]) < 1:
			self.errors["tags"] = gettext("At least one tag is required.")


		return len(self.errors) == 0

	def find_popular(self, limit=5, language=None, skip=0):
		query = dict()
		if language is not None:
			query["language"] = language
		return self.find(query, sort=[("likes_count", -1)], limit=limit, skip=skip)

	def find_new(self, limit=5, language=None, skip=0):
		query = dict()
		if language is not None:
			query["language"] = language
		return self.find(query, sort=[("_id", -1)], limit=limit, skip=skip)

	def find_random(self, limit=5, language=None):
		rand = self.get_random_value(int, 5)
		query = {"random" : {"$gte" : rand}}
		if language is not None:
			query["language"] = language
		rand_records = self.find(query,sort=[("random", 1)], limit=limit)
		count = rand_records.count()
		if count < limit:
			lt_rand_records = self.find({"random" : {"$lt" : rand}},
				sort=[("random", -1)],
				limit=limit-count)
			if lt_rand_records is not None and lt_rand_records.count() > rand_records.count():
				return lt_rand_records
			else:
				return rand_records
		return rand_records

	def find_startswith(self, alphabet, limit=5, language=None, skip=0):
		query = {"phrase" : {"$regex" : "^"+alphabet}}
		if language is not None:
			query["language"] = language
		return self.find(query, sort=[("phrase", 1)], limit=limit, skip=skip)

	def search(self, term, limit=5, language=None, skip=0):
		query = dict()
		if language is not None:
			query["language"] = language
		return super(self.__class__, self).search(term, query, limit=limit)

	def like(self, word_id):
		self.update(
			{"_id" : ObjectId(word_id)}, 
			{
				"$inc" : {"likes_count" : 1},
				"$push" : {"likes" : {"user_id" : ObjectId(self.user_id), "date_liked" : datetime.utcnow().isoformat()}}
			}
		)

	def dislike(self, word_id):
		self.update(
			{"_id" : ObjectId(word_id)}, 
			{
				"$inc" : {"dislikes_count" : -1},
				"$push" : {"dislikes" : {"user_id" : ObjectId(self.user_id), "date_liked" : datetime.utcnow().isoformat()}}
			}
		)

	def view(self, word_id):
		self.update(
			{"_id" : ObjectId(word_id)}, 
			{
				"$inc" : {"views_count" : -1},
				"$push" : {"views" : {"user_id" : ObjectId(self.user_id), "date_viewed" : datetime.utcnow().isoformat()}}
			}
		)

	def change_status(self, word_id, new_status):
		if new_status in self.STATUS.values():
			self.update(
				{"_id" : ObjectId(word_id)}, 
				{
					"$set" : {"status" : new_status}
				}
			)
			return True
		else:
			return False

	def update_freshly_loggedin_user_activity(self, old_user_id, new_user_id):
		self.update(
			{"user_id" : ObjectId(old_user_id)}, 
			{
				"$set" : {"user_id" : ObjectId(new_user_id)}
			}
		)
		self.update(
			{"views.user_id" : ObjectId(old_user_id)}, 
			{
				"$set" : {"views.$.user_id" : ObjectId(new_user_id)}
			},
			{ "multi" : True}
		)
		self.update(
			{"likes.user_id" : ObjectId(old_user_id)}, 
			{
				"$set" : {"likes.$.user_id" : ObjectId(new_user_id)}
			},
			{ "multi" : True}
		)
		self.update(
			{"dislikes.user_id" : ObjectId(old_user_id)}, 
			{
				"$set" : {"dislikes.$.user_id" : ObjectId(new_user_id)}
			},
			{ "multi" : True}
		)


class Language(MongoDB):
	"""
	Language model for manipulating language collection
	structure = {
		"language" : unicode,
		"language_code" : unicode,
		"status" : Word.STATUS["approved"],
		"word_count" : int
 	}
	"""
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

	__collection__ = 'languages'

	def upsert(self, language):
		return self.update({"language" : language}, 
					{"$set" : {"language" : language, "status" : Word.STATUS["approved"]},
					  "$inc" : {"word_count" : 1}
					},
					True
					)

	def change_status(self, language_id, new_status):
		self.update({"_id" : ObjectId(language_id)}, 
					{"$set" : {"status" : new_status}}
					)

	def get(self):
		return self.find(sort={"word_count" : -1})