from meded import app
from meded import user
from meded import login_manager
from meded import query_db

@login_manager.user_loader
def load_user(userid):
	return user.get(userid)

def validate_user(username, password):
	val = query_db('SELECT user_id FROM users WHERE username=? AND password=?', (username, password), True)
	if val is None:
		return None
	else:
		return val[0]