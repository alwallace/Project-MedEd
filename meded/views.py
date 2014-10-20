from meded import app
from meded import login
from meded import user
from meded import quiz
from flask import request
from flask import render_template
from flask import flash, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
import json


@app.route('/')
@login_required
def indexRoute():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def loginRoute():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		uid = login.validate_user(username, password)
		if uid:
			login_user(user.get(uid))
			flash("Logged in successfully")
			return redirect(request.args.get("next") or url_for("indexRoute"))
	elif request.method == 'GET':
		return render_template("login.html")

@app.route('/get/normal_quiz', methods=['GET'])
def getNormalQuizRoute():
	return json.dumps(quiz.getNormalQuiz())