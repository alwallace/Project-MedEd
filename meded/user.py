import json
from meded import app
from meded import query_db

def get(userid):
	val = query_db("SELECT username, password FROM users WHERE user_id=?", (userid,), True)
	if val is not None:
		return User(userid, val[0], val[1])
	else:
		return None

def getName(userid):
	val = query_db("SELECT username FROM users WHERE user_id=?", (userid,), True)


class User():
	def __init__(self, uid, username, password):
		self.uid = uid
		self.username = username
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.uid)

	def __repr__(self):
		return '<User ' + self.username + '>'