from meded import query_db, commit_db, lastid_db
from flask import url_for
from meded import constants
import random

def editCaseValues(caseID, values):
	response = []
	for value in values:
		commit_db("UPDATE case_values SET value=? WHERE case_value_id=?", (values['value'], values['caseValueID']))
	reponse.append('done')
	return response