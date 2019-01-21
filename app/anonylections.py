from app import app, db
from app.models import User, Election, Choice, Vote, Token

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'User':User, 'Election':Election, 'Choice':Choice, 'Vote':Vote, 'Token': Token}
