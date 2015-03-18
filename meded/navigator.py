from meded import query_db, commit_db, lastid_db
from flask import url_for
from meded import constants
import random

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

		if v == 'history' or v == 'history_adequate':
			response[0][v] = row[1].split(';')
		else: 
			response[0][v] = row[1]
	return response

def getCaseImaging(caseID):
	response = [{}]
	important_values = ['imaging', 'imaging_normal', 'imaging_explanation']
	for v in important_values:
		row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, v), True)
		if v == 'imaging':
			response[0][v] = row[1].split(';')
			for i in range(0, len(response[0][v])):
				response[0][v][i] = url_for('static', filename='images/' + response[0][v][i])
		elif v == 'imaging_normal':
			response[0][v] = row[1].split(';')
		else:
			response[0][v] = row[1]

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

def getRandomNormalCXR():
	normalImageCount = int(query_db('SELECT COUNT(images.image_id) FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id', (constants.NORMAL_IMAGE_TAG,), True)[0])
	normalResult = query_db('SELECT images.image_id, images.filename FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id LIMIT 1 OFFSET ' + str(random.randint(0, normalImageCount - 1)), (constants.NORMAL_IMAGE_TAG,), True)

	response = {"image_id":normalResult[0], "image_loc":url_for('static', filename='images/' + normalResult[1]) }
	return response

def createCase(navItemSuperID):
	name = "New Case"
	description = "New case description"
	descriptionImage = "newcase.jpg"

	commit_db("INSERT INTO nav_items (case_id, nav_item, nav_item_super_id) VALUES (?,?,?)")
	navItemID = lastid_db()

	commit_db("INSERT INTO cases (nav_item_id, nav_item_id, name, description, description_image) VALUES (?,?,?,?)", (navItemDB, navItemSuperID, name, description, descriptionImage))


	reponse = {"case_id":lastID}
	return response

def deleteCase(caseID):
	commit_db("DELETE FROM nav_items WHERE case_id=?", (caseID,))
	commit_db("DELETE FROM cases WHERE case_id=?", (caseID,))
	commit_db("DELETE FROM case_values WHERE case_id=?", (caseID,))

	response = {'status':'done'}
	return response