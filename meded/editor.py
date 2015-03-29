from meded import query_db, commit_db, lastid_db
from flask import url_for
from meded import constants
import random

def editCaseValues(caseID, values, prop):
	response = {}
	for value in values:
		commit_db("UPDATE case_values SET value=? WHERE case_value_id=?", (value['value'], value['caseValueID']))
	commit_db("UPDATE cases SET name=?, description=?, description_image=? WHERE case_id=?", (prop['caseName'], prop['caseDescription'], prop['caseImage'], caseID))
	commit_db("UPDATE nav_items SET nav_item=?, nav_item_super_id=? WHERE case_id=?", (prop['caseNavName'], prop['caseNavSuperID'], caseID))

	response['status'] = 'Case Edit: Completed Successfully'
	return response

def createCase():
	DEFAULT_CASE_VALUES = ['history',
						   'history_adequate',
						   'history_explanation',
						   'imaging',
						   'imaging_normal',
						   'imaging_explanation',
						   'report'
						   'report_adequate',
						   'report_explanation',
						   'summary',
						   'test_question_answer']

	name = "New Case"
	description = "New case description"
	descriptionImage = "newcase.jpg"

	commit_db("INSERT INTO cases (name, description, description_image) VALUES (?,?,?)", (name, description, descriptionImage))
	caseID = lastid_db()
	commit_db("INSERT INTO nav_items (case_id, nav_item, nav_item_super_id) VALUES (?,?,?)", (caseID, '', '',))

	for item in DEFAULT_CASE_VALUES:
		commit_db("INSERT INTO case_values (case_id, value, value_type) VALUES (?,?,?)", (caseID, "", item))
		if item is 'test_question_answer':
			for count in range(1, 10):
				commit_db("INSERT INTO case_values (case_id, value, value_type) VALUES (?,?,?)", (caseID, "", item))

	response = {"case_id":lastid_db()}
	return response

def deleteCase(caseID):
	commit_db("DELETE FROM nav_items WHERE case_id=?", (caseID,))
	commit_db("DELETE FROM cases WHERE case_id=?", (caseID,))
	commit_db("DELETE FROM case_values WHERE case_id=?", (caseID,))

	response = {'status':'done'}
	return response