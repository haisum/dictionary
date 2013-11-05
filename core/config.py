"""
Config file, override as you like! Keep secret key secret
"""
class Config(object):
	DEBUG = False
	TESTING = False
	SECRET_KEY  = '\xa1\x8b\x0fg\xcbO\xfbV\x1cJ\xf4\x7f\xf5N\xfd\xff\xe5a\xff\x8eTEzi'
	MONGODB_DATABASE = "worldslangs"

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	MONGODB_DATABASE = "worldslangs_test"
	MONGODB_HOST = "localhost"