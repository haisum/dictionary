from flask import render_template, abort, url_for, current_app, g, request, redirect
from jinja2 import TemplateNotFound
from flask import Blueprint
from core import app
from modules.word.models import Word
from datetime import datetime
import json
import string

bp_word = Blueprint('bp_word', __name__, template_folder="templates")

@bp_word.route("/")
def home():
	"""
	business logic for home page
	"""
	try:
		word = Word(g.user["_id"])
		return render_template("home.html", words = word.find_popular(10))
	except TemplateNotFound:
		app.logger.error("template word/home.html not found")
		abort(404)

@bp_word.route("/new")
def new_words():
	"""
	business logic for home page
	"""
	try:
		word = Word(g.user["_id"])
		return render_template("home.html", words = word.find_new(10))
	except TemplateNotFound:
		app.logger.error("template word/home.html not found")
		abort(404)

@bp_word.route("/random")
def random_words():
	"""
	business logic for home page
	"""
	try:
		word = Word(g.user["_id"])
		return render_template("home.html", words = word.find_random(10))
	except TemplateNotFound:
		app.logger.error("template word/home.html not found")
		abort(404)


@bp_word.route("/start-with/<alphabet>")
def alpha(alphabet):
	"""
	business logic for home page
	"""
	try:
		word = Word(g.user["_id"])
		return render_template("home.html", words = word.find_startswith(alphabet.lower(),10))
	except TemplateNotFound:
		app.logger.error("template word/home.html not found")
		abort(404)

@bp_word.route("/add", methods=["GET"])
def show_add_form():
	"""
	Shows add word form
	"""
	try:
		return render_template("add_word.html")
	except TemplateNotFound:
		app.logger.error("template word/add_word.html not found")
		abort(404)

@bp_word.route("/add", methods=["POST"])
def add_word():
	"""
	add slang to database
	"""
	word = Word(g.user["_id"])
	try:
		data = {
			'language': request.form.get("language"),
			'local': request.form.get("local"),
			'phrase' : request.form.get("phrase"),
			'definition' : request.form.get("definition"),
			'example' : request.form.get("example"),
			'tags' : [tag.strip() for tag in request.form.get("tags").split(",")],
			'likes' : [],
			'dislikes' : [],
			'likes_count' : 0,
			'dislikes_count' : 0,
			'views' : [],
			'views_count' : 0,
			'date_added' : datetime.utcnow().isoformat(),
			'status' : Word.STATUS["approved"],
			'user_id' : g.user["_id"],
			'user_nick' : "",
			'random' : word.get_random_value(int, 5)
		}
		word_id = word.insert_word(data)
		if word_id is None:
			return render_template("add_word.html", error="Error(s) occured in validation", errors = word.errors)
		else:
			return redirect(url_for("bp_word.show_add_form", success="Word inserted successfully."))
	except KeyError as keys:
		return render_template("add_word.html", error="Required form field missing: " + keys[0])
	except Exception as errors:
		return render_template("add_word.html", error="Unknown error occured. Contact site admin to report this." + json.dumps(errors.args))


app.register_blueprint(bp_word)
