from meded import query_db, commit_db, lastid_db
from flask import url_for


def getNavItems(superID):
	response = []
	rows = query_db("SELECT nav_item_id, nav_item FROM nav_items WHERE nav_item_super_id=?", (superID,))
	for row in rows:
		response.append({'id':row[0], 'value':row[1], 'subitems':getNavItems(row[0])})
	return response

def getCaseFromNavID(navID):
	response = []
	row = query_db("SELECT case_id FROM cases WHERE nav_item_id=?", (navID,), True)
	response.append({'caseID':row[0]})
	return response

def getCaseBrief(caseID):
	response = []
	row = query_db("SELECT name, description, description_image FROM cases WHERE case_id=?", (caseID,), True)
	response.append({'name':row[0], 'description':row[1], 'description_image':row[2]})
	return response

def getCaseTest(caseID):
	response = []
	rows = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, "test_question_answer"))
	for row in rows:
		qasplit = row[1].split(';')
		response.append({'case_value_id':row[0], 'question':qasplit[0], 'answer':qasplit[1]})
	return response

def getCaseHistory(caseID):
	response = [{}]
	important_values = ['history', 'history_adequate', 'history_explanation']
	for v in important_values:
		row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, v), True)
		response[0][v] = row[1]
	return response

def getCaseImaging(caseID):
	response = [{}]
	important_values = ['imaging', 'imaging_normal', 'imaging_explanation']
	for v in important_values:
		row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, v), True)
		response[0][v] = row[1]

	response[0]['imaging'] = url_for('static', filename='images/' + response[0]['imaging'])
	return response

def getCaseReport(caseID):
	response = [{}]
	important_values = ['report', 'report_adequate', 'report_explanation']
	for v in important_values:
		row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, v), True)
		response[0][v] = row[1]
	return response

def getCaseSummary(caseID):
	response = [{}]
	important_values = ['summary']
	for v in important_values:
		row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, v), True)
		response[0][v] = row[1]
	return response
