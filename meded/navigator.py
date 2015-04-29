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

def getCaseList():
	response = []
	rows = query_db("SELECT case_id, name, description FROM cases")
	for row in rows:
		response.append({'caseID':row[0], 'name':row[1], 'description':row[2]})
	return response

def getCaseFromNavID(navID):
	response = []
	row = query_db("SELECT cases.case_id FROM cases, nav_items WHERE nav_items.nav_item_id=? AND nav_items.case_id=cases.case_id", (navID,), True)
	response.append({'caseID':row[0]})
	return response

def getCaseInfo(caseID):
	response = {}
	name, desc, image = query_db("SELECT name, description, description_image FROM cases WHERE case_id=?", (caseID,), True)
	superID, navName = query_db("SELECT nav_item_super_id, nav_item FROM nav_items WHERE case_id=?", (caseID,),True)
	response['name']=name
	response['description']=desc
	response['description_image']=image
	response['navSuperID']=superID
	response['navName']=navName

	rows = query_db("SELECT case_value_id, value_type, value FROM case_values WHERE case_id=?", (caseID,))
	values = []
	for row in rows:
		values.append({'caseValueID':row[0], 'value':row[1], 'data':row[2]})
	response['values'] = values
	return response

def getCaseBrief(caseID):
	response = []
	row = query_db("SELECT name, description, description_image FROM cases WHERE case_id=?", (caseID,), True)
	response.append({'name':row[0], 'description':row[1], 'description_image':url_for('static', filename='images/' + row[2])})
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
	# Get imaging information
	row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, 'imaging'), True)
	response[0]['imaging'] = row[1].split(';')
	for i in range(0, len(response[0]['imaging'])):
		response[0]['imaging'][i] = url_for('static', filename='images/' + response[0]['imaging'][i])
	# Get the imaging_normal information
	row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, 'imaging_normal'), True)
	response[0]['imaging_normal'] = row[1].split(';')
	# Get the imaging_expalanation information
	row = query_db("SELECT case_value_id, value FROM case_values WHERE case_id=? AND value_type=?", (caseID, 'imaging_explanation'), True)
	response[0]['imaging_explanation'] = row[1]

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
