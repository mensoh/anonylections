import random, string
from app import app, db
from app.forms import LoginForm, ElectionForm
from app.models import User, Election, Choice, Token, Vote
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func, desc
from flask_mail import Mail, Message

mail = Mail(app)

# Check if user owns the election with eid
def CheckOwner(eid):
	e = Election.query.filter_by(id=eid).first()
	if e:
		if e.ownedby.username == current_user.username:
			return True
	else:
		return False

# Add election 
def AddElection(name, description):
	# Check if name is already in use or not for this user
	election = Election.query.filter_by(name=name, owner=current_user.get_id()).first()
	if election is None:
		e = Election(name=name, description=description,owner=current_user.get_id(), status=0, resulturl=GenerateResultUrl())
		db.session.add(e)
		db.session.commit()
		return True
	else:
		return False 
		
# Delete election
def DeleteElection(id):
	if CheckOwner(id):
		e = Election.query.filter_by(id=id).first()
		db.session.delete(e)
		db.session.commit()
		return True
	else:
		return False

# Add choice to election
def AddChoice(eid, choice):
	if CheckOwner(eid):
		print('CheckOwner')
		# Check if choice is already in use or not
		c = Choice.query.filter_by(election=eid, choice=choice).first()
		if c is None:
			print('hello')
			c = Choice(choice=choice, election=eid)
			db.session.add(c)
			db.session.commit()
			return True 
	else:
		return False

# Delete choice from election
def DeleteChoice(eid, cid):	
	if CheckOwner(eid):
		c = Choice.query.filter_by(id=cid).first()
		if c:
			db.session.delete(c)
			db.session.commit()
			return True
	else:
		return False

# Get all elections for user
def GetElections(username):
	u = User.query.filter_by(username=username).first()
	e = u.elections.all()
	return e

# Get all choices for election id
def GetChoices(eid):
	c =  Choice.query.filter_by(election=eid).all()
	return c

# Get results for election id
def GetResults(eid):
	r = Vote.query.filter_by(election=eid).order_by(Vote.choice).all()
	return r

# Register vote for election
def RegisterVote(cid, token):
	t = Token.query.filter_by(token=token).first()
	if t is not None:
		c = Choice.query.filter_by(id=cid).first()
		e = Election.query.filter_by(id=t.election).first()

		# Check if all the values return results
		if c is not None and e is not None:
			# Check if the token & choice match the election
			if c.election == e.id and t.election == e.id:
				# register the vote in Vote
				confirmcode=GenerateConfirmCode()
				v = Vote(choice=c.id, election=e.id, confirmcode=confirmcode)
				# Add the vote
				db.session.add(v)
				# Delete the token
				db.session.delete(t)
				# Commit
				db.session.commit()
				return confirmcode
			else:
				return False
	else:
		return False

# Generate confirmation code to be shown to user after voting
def GenerateConfirmCode():
	allchar = string.digits
	confirmcode = "".join(random.choice(allchar) for x in range(random.randint(5,5)))
	# Make sure it's unique
	cc = Vote.query.filter_by(confirmcode=confirmcode).first()
	if cc is None:
		return confirmcode
	else:
		GenerateConfirmCode()

# Generate colors for the result graphs
def GetColors(n):
	if n == 0:
		n=1
	max_value = 16581375 #255**3
	interval = int(max_value / n)
	colors = [hex(I)[2:].zfill(6) for I in range(100, max_value, interval)]  
	return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]

# Generate random url for sharing election results
def GenerateResultUrl():
	allchar = string.ascii_letters + string.digits
	resulturl = "".join(random.choice(allchar) for x in range(random.randint(50,50)))
	# Make sure it's unique
	e = Election.query.filter_by(resulturl=resulturl).first()
	if e is None:
		return resulturl
	else:
		GenerateResultUrl()

# Send invitation mail
def SendMails(sender, subject, addresses, message, eid, url):
	addresses = addresses.split('\r\n')
	print(addresses)
	for address in addresses:
		address.strip()
		if address != '':
			print("Sent message to: " + address)
			msg = Message(subject, sender=sender, recipients=address.split())
			msg.body = message.replace('!link!', url+'&token='+GenerateVotingToken(eid))
			mail.send(msg)
	return True

# Generate random tokens needed to vote (sent through invitation)
def GenerateVotingToken(eid):
	allchar = string.ascii_letters + string.digits
	token = "".join(random.choice(allchar) for x in range(random.randint(50,50)))
	t = Token.query.filter_by(token=token, election=eid).first()
	if t is None:
		t = Token(token=token, election=eid)
		db.session.add(t)
		db.session.commit()
		return token
	else:
		GenerateVotingToken(eid)



