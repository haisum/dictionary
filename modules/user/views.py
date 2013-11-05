from flask import render_template, abort, url_for, request, redirect, session
from jinja2 import TemplateNotFound
from flask import Blueprint
from core import app, oid
from modules.user.models import User

import json
from datetime import datetime

bp_user = Blueprint('bp_user', __name__, template_folder="templates")

@bp_user.route("/login", methods=['GET', 'POST'])
@oid.loginhandler
def login():
	"""
	show login page
	"""
	try:
		if request.args.get("openid_identifier") is not None:
			openid = request.args.get("openid_identifier")
			return oid.try_login(openid, ask_for=['email', 'fullname',
												  'nickname', 'language', 'image', 'timezone'])
		else:
			return render_template("login.html", next=oid.get_next_url(), error = oid.fetch_error())
	except TemplateNotFound:
		app.logger.error("template user/login.html not found")
		abort(404)

@oid.after_login
def create_or_login(resp):
	session['openid'] = resp.identity_url

	user_model = User()
	user = user_model.find({'email' : resp.email})
	if user is not None:
		user_data = structure = {
			"nick" : resp.nickname or resp.fullname,
			"fullname" : resp.fullname,
			"email" : resp.email,
			"favourites" : [],
			"roles" : [],
			"reputation" : 1,
			"logins" : [{
				'ip' : request.remote_addr,
				'date_loggedin' : datetime.utcnow().isoformat(),
			}],
			"about" : "",
			"language" : resp.language,
			"timezone" : resp.timezone
		}
		user_data["_id"] = user_model.insert(user_data)
		g.user = user
		return redirect(oid.get_next_url())	   
	g.user = user
	return redirect(url_for("bp_word.home"))

@bp_user.route("/profile", methods=["GET"])
def user_profile():
	return json.dumps(request.args)

app.register_blueprint(bp_user)