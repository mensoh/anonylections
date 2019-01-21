from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    elections = db.relationship('Election', backref='ownedby', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def is_admin(self):
    	if self.admin ==1:
    		return True
    	else:
    		return False
    
    def get_id(self):
    	return self.id

    def electioncount(self):
    	return self.elections.count()


class Election(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), index=True, unique=True)
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	description = db.Column(db.String(256), index=True, unique=False)
	startdate = db.Column(db.String(256))
	enddate = db.Column(db.String(256))
	resulturl = db.Column(db.String(256))
	shareurl = db.Column(db.Integer)
	status = db.Column(db.Integer)
	invites = db.Column(db.Integer)
	choice = db.relationship('Choice', backref='choices', lazy='dynamic', cascade="all, delete-orphan")

	def __repr__(self):
		return '<Election {}>'.format(self.name)


class Token(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	token = db.Column(db.String(120), index=True, unique=True)
	election = db.Column(db.Integer, db.ForeignKey('election.id'))


class Choice(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	choice = db.Column(db.String(120), index=True, unique=True)
	election = db.Column(db.Integer, db.ForeignKey('election.id'))
	votes = db.relationship('Vote', backref='votes', cascade="all, delete-orphan")

	def __repr__(self):
		return '<Choice {}>'.format(self.choice)

	def votecount(self):
		return Vote.query.filter_by(choice=self.id, election=self.election).count()


class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	choice = db.Column(db.Integer, db.ForeignKey('choice.id'))
	election = db.Column(db.Integer, db.ForeignKey('election.id'))
	confirmcode = db.Column(db.String(120), index=True, unique=True)
	label = db.relationship('Choice', backref='label')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))