from app import app, db
from app.forms import LoginForm, ElectionForm
from app.models import User, Election, Choice, Token
from flask_login import current_user, login_user, logout_user, login_required

def AddUser(username, email, password, confirmpassword, admin):

	# Does the user already exist?
	u = User.query.filter_by(username=username).first()
	if u is not None:
		return False
	else:
		if password == confirmpassword and password != '':
			u = User(username=username, email=email, admin=admin)
			u.set_password(password)
			db.session.add(u)
			db.session.commit()
			return True
		else:
			return False

def UpdateUser(uid, username, email, password, confirmpassword, admin):
	u = User.query.filter_by(id=uid).first()
	if u is None:
		return False
	else:
		u.username = username
		u.email = email
		u.admin = admin
		if password == confirmpassword:
			if password != '':
				u.set_password(password)
		else:
			return False 
		db.session.commit()
		return True

def DeleteUser(uid):
	u = User.query.filter_by(id=uid).first()
	if u is not None:
		db.session.delete(u)
		db.session.commit()
		return True
	else:
		return False
