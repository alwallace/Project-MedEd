from meded import app, login, user, constants, navigator
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
####
# /EDIT
####
@app.route('/edit')
@login_required
def editRoute():
	return render_template("edit_index.html")

@app.route('/edit/case', methods=['GET', 'POST'])
@login_required
def editCaseRoute():
	if request.method == 'GET':
		return render_template("case_edit.html")
	elif request.method == 'POST':
		caseID = request.args.get("caseID")
		caseValues = json.loads(request.args.get("caseID"), request.args.get("caseValues"))
		return json.dumps(editor.setCase(caseID, caseValues))

####
# /GET
####
@app.route('/get/case_list')
@login_required
def getCaseListRoute():
	return json.dumps(navigator.getCaseList())

@app.route('/get/case_from_navid', methods=['POST'])
@login_required
def getCaseFromNavIDRoute():
	return json.dumps(navigator.getCaseFromNavID(request.form['navID']))

@app.route('/get/caseInfo', methods=['POST'])
@login_required
def getCaseInfoRoute():
	return json.dumps(navigator.getCaseInfo(request.form['caseID']))

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

@app.route('/new/case', methods=['GET', 'POST'])
@login_required
def createCaseRoute():
	return json.dumps(navigator.createCase())

@app.route('/delete/case', methods=['POST'])
@login_required
def deleteCaseRoute():
	return json.dumps(navigator.deleteCase(request.form['caseID']))