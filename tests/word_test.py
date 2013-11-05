import os, json
import unittest
from tests import app, ctx
from modules.word.views import home, show_add_form
from modules.word.models import Word, Language
from core.database import db
from datetime import datetime
# from pymongo.objectid import ObjectId

class ModelWordTestCase(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		self.model = Word(user_id="haisum")
		super(self.__class__, self).__init__(*args, **kwargs)

	def setUp(self):
		self.model.insert(self.generate_fixtures(), False)
	
	def test_insert(self):
		fixtures = self.generate_fixtures(5)
		for data in fixtures:
			slang_id = self.model.insert_slang(data)

			self.assertTrue(slang_id is not None,  json.dumps(self.model.errors))
			insertedWord = db.words.find_one({'_id' : slang_id})
			"""
			Correct Validation
			"""
			self.assertTrue(insertedWord["language"])
			self.assertTrue(insertedWord["status"])
			"""
			If english, only phrase is required but  in case of other language
			either phrase and translation is required or local script and translation is required
			"""
			self.assertTrue((insertedWord["language"].lower() == "english" and insertedWord["phrase"]) or (insertedWord["phrase"] and insertedWord["translation"]))
			"""
			Correct data inside db
			"""
			self.assertEqual(insertedWord["language"], data["language"].lower())
			self.assertEqual(insertedWord["status"], data["status"])
			self.assertEqual(insertedWord["translation"], data["translation"])
			self.assertEqual(insertedWord["views"][0]["user_id"], data["views"][0]["user_id"])
			self.assertEqual(insertedWord["views"][0]["date_viewed"], data["views"][0]["date_viewed"])

			self.assertEqual(insertedWord["translation"], data["translation"])

			self.assertEqual(len(insertedWord["views"]), data["views_count"])
			self.assertEqual(len(insertedWord["tags"]), len(data["tags"]))
			"""
			language exists
			"""
			self.assertTrue(db.languages.find({"language" : insertedWord["language"]}) is not None)

	"""
	@todo  not a good method for popular words! need to consider likes and recent additions
	"""
	def test_select_popular(self):
		popular_words = self.model.find_popular(limit=5)
		words_from_db = db.words.find().sort([("likes_count", -1)]).limit(5)

		self.assertTrue(words_from_db.count(True) <= 5, words_from_db.count(True))
		self.assertTrue(popular_words.count(True) <= 5, popular_words.count(True))
		"""
		Words returned from db are exactly same as returned by model
		"""
		for index, item in enumerate(popular_words):
			self.assertTrue(words_from_db[index]["phrase"] == item["phrase"])
		"""
		Popular from particular language
		"""
		popular_words = self.model.find_popular(language="urdu")
		self.assertTrue( popular_words.count() <= 5 )
		words_from_db = db.words.find({"language" : words_from_db[1]["language"]}).sort([("likes_count", -1)]).limit(5)
		"""
		Words returned from db are exactly same as returned by model
		"""
		for index, item in enumerate(popular_words):
			self.assertTrue(words_from_db[index]["phrase"] == item["phrase"])


	def test_select_alphabet(self):
		words_startwith_a = self.model.find_startswith("a")
		self.assertTrue(words_startwith_a.count() <= 5 )
		words_from_db = db.words.find({"phrase" : {"$regex" : "^a"}}).limit(5)
		"""
		Words returned from db are exactly same as returned by model
		"""
		for index, word in enumerate(words_startwith_a):
			self.assertTrue("phrase" in word and word["phrase"] == words_from_db[index]["phrase"])

	def test_change_status(self):
		pass

	def test_like(self):
		pass

	def test_dislike(self):
		pass

	def test_add_detail(self):
		pass

	def tearDown(self):
		db.languages.remove()
		db.words.remove()

	def generate_fixtures(self, count=15):
		return [self.model.generate_fixture(self.model.structure) for x in xrange(0, count)]

if __name__ == '__main__':
	unittest.main()