import os, base64, pymongo
from flask import Flask, g, request, session
from flask_openid import OpenID
from flask.ext.babel import Babel
"""
Naming default templates folder to layouts because it will contain base templates and layouts,
real content will be inside <module_name>/templates folder which will extend templates in layouts folder
"""
app = Flask(__name__, static_folder="../static", template_folder="../layouts")

"""
Config can be either of 
DevelopmentConfig
ProductionConfig
TestingConfig
"""
app.config.from_object('core.config.DevelopmentConfig')

"""
Internationalization support
"""
babel = Babel(app)

"""
OpenID instance
"""
openid_store = "logs"
oid = OpenID(app, openid_store)

"""
Helper modules for app
"""
from core import context_processors, loggers

"""
Create cookie to track activities if user is not logged in
Value in this cookie will be used as temporary userid in words, descriptions, views, likes and dislikes
"""
@app.before_request
def create_temp_userid_cookie():
	if 'openid' not in session:
		if request.cookies.get("tempuid") is None:
			g.user = {"_id" : os.urandom(4)}
		else:
			g.user = {"_id" : request.cookies.get("tempuid")}

@app.after_request
def create_temp_userid_cookie_response(response):
	if 'openid' not in session and hasattr(g, "user"):
		response.set_cookie("tempuid", g.user["_id"], max_age = 365*24*60*60)
	return response

"""
import error handlers
"""
from core import error_handlers

"""
Import all views.
To disable a url, simply don't include its view and remove url_for() references in templates
This must be in the end of this file, otherwise there will be circular dependencay problems inside views
"""
import modules.word.views
import modules.user.views