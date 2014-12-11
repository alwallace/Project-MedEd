from meded import app, login, user, quiz, constants, navigator
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
import json

@app.route('/', methods=['GET', 'POST'])
@login_required
def indexRoute():
	if request.method == 'POST':
		response = navigator.getNavItems(0)
		return json.dumps(response)
	elif request.method == 'GET':
		return render_template("index.html")

@app.route('/pretest', methods=['GET', 'POST'])
@login_required
def pretestRoute():
	if request.method == 'POST':
		return json.dumps(navigator.getCaseTest(request.form['caseID']))
	elif request.method == 'GET':
		return render_template("pretest.html")

@app.route('/history', methods=['GET', 'POST'])
@login_required
def historyRoute():
	if request.method == 'POST':
		return json.dumps(navigator.getCaseHistory(request.form['caseID']))
	elif request.method == 'GET':
		return render_template("history.html")

@app.route('/imaging', methods=['GET', 'POST'])
@login_required
def imagingRoute():
	if request.method == 'POST':
		return json.dumps(navigator.getCaseImaging(request.form['caseID']))
	elif request.method == 'GET':
		return render_template("imaging.html")

@app.route('/report', methods=['GET', 'POST'])
@login_required
def reportRoute():
	if request.method == 'POST':
		return json.dumps(navigator.getCaseReport(request.form['caseID']))
	elif request.method == 'GET':
		return render_template("report.html")

@app.route('/summary', methods=['GET', 'POST'])
@login_required
def summaryRoute():
	if request.method == 'POST':
		return json.dumps(navigator.getCaseSummary(request.form['caseID']))
	elif request.method == 'GET':
		return render_template("summary.html")

@app.route('/posttest', methods=['GET', 'POST'])
@login_required
def posttestRoute():
	if request.method == 'POST':
		return json.dumps(navigator.getCaseTest(request.form['caseID']))
	elif request.method == 'GET':
		return render_template("posttest.html")

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

@app.route('/logout')
@login_required
def logoutRoute():
	logout_user()
	return redirect('/login')

@app.route('/quiz/normals', methods=['GET'])
@login_required
def quizNormalsRoute():
	return render_template("quiz_normals.html")

@app.route('/get/case_from_navid', methods=['POST'])
@login_required
def getCaseFromNavIDRoute():
	return json.dumps(navigator.getCaseFromNavID(request.form['navID']))

@app.route('/get/normal_quiz', methods=['GET'])
@login_required
def getNormalQuizRoute():
	return json.dumps(quiz.getNormalQuiz())

@app.route('/get/random_normal_cxr', methods=['GET'])
@login_required
def getRandomNormalCXRRoute():
	location = navigator.getRandomNormalCXR()['image_loc']
	response = "<html><img src='" + location + "' width=100% /></html>"
	return response

@app.route('/get/case_brief', methods=['POST'])
@login_required
def getCaseBriefRoute():
	return json.dumps(navigator.getCaseBrief(request.form['caseID']))

@app.route('/get/case_test', methods=['POST'])
@login_required
def getCaseTestRoute():
	return json.dumps(navigator.getCaseTest(request.form['caseID']))

@app.route('/get/case_history', methods=['POST'])
@login_required
def getCaseHistoryRoute():
	return json.dumps(navigator.getCaseHistory(request.form['caseID']))

@app.route('/get/case_imaging', methods=['POST'])
@login_required
def getCaseImagingRoute():
	return json.dumps(navigator.getCaseImaging(request.form['caseID']))

@app.route('/get/case_report', methods=['POST'])
@login_required
def getCaseReportRoute():
	return json.dumps(navigator.getCaseReport(request.form['caseID']))

@app.route('/get/case_summary', methods=['POST'])
@login_required
def getCaseSummaryRoute():
	return json.dumps(navigator.getCaseSummary(request.form['caseID']))