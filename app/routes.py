from flask import render_template, flash, redirect, url_for, request, Markup
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func
import random, re

from app import app, db
from app.models import User, Election, Choice, Token, Vote
from app.elections import AddElection, DeleteElection, AddChoice, DeleteChoice, GetElections, CheckOwner, GetColors,GetChoices, RegisterVote, GetResults, SendMails
from app.usermgt import AddUser, UpdateUser, DeleteUser
from app.forms import ElectionForm, LoginForm


# Show the index page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = ElectionForm()
	if form.validate_on_submit():
		if not AddElection(form.electionname.data, form.description.data):
			flash('Election name already in use')
		return redirect(url_for('index'))
	e=GetElections(current_user.username)
	return render_template('index.html', elections=e, form=form, page='home')


# Change election settings (e.g. open/close, share url, delete election)
@app.route('/election', methods=['GET', 'POST'])
@login_required
def election():
	if request.method == 'POST':
		action = request.form['action']
		eid = request.form['id']
		print('made it')

		# Check if user is owner of election before we do anything
		if not CheckOwner(eid):
			flash('You do not own an election by that id')
			return redirect(url_for('index'))

		if action == 'AddChoice':
			if not AddChoice(eid, request.form['choice']):
				flash('Error adding choice, does it already exist?')
			return redirect(url_for('election', id=eid))

		elif action == 'shareAfterVote':
			election = Election.query.filter_by(id=eid).first()
			if request.form['shareAfterVote'] == '0':
				print ('share')
				election.shareurl = 1
				db.session.commit()
				return redirect(url_for('election',id=eid))
			elif request.form['shareAfterVote'] == '1':
				print ('dont')
				election.shareurl = 0
				db.session.commit()
				return redirect(url_for('election', id=eid))	
	else:
		eid = request.args.get('id')
	
	# Check if user is owner of election before we do anything
	if not CheckOwner(eid):
		flash('You do not own an election by that id')
		return redirect(url_for('index'))
	
	election = Election.query.filter_by(id=eid).first()
	
	# Check if we need to change the status
	if request.args.get('changestatus') == 'open':
		election.status=1
		db.session.commit()
		flash('Election opened')
		return redirect(url_for('election', id=eid))
	
	if request.args.get('changestatus') == 'close':	
		election.status=0
		db.session.commit()
		flash('Election closed')
		return redirect(url_for('election', id=eid))

	# Check if we got a delete request
	if request.args.get('delete') == '1':
		DeleteElection(eid)
		flash('election deleted')
		return redirect(url_for('index'))

	c = GetChoices(eid)
	e = GetElections(current_user.username)
	r = GetResults(eid)
	invites = election.invites
	votes = Vote.query.filter_by(election=eid).count()
	return render_template('election.html', results=r, choices=c, elections=e, election=election, invites=invites, votes=votes, colors=GetColors(len(c)))


#Update election settings
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
	if request.method=='POST':		
		if request.form['name'] and request.form['desc'] and request.form['eid']:
			eid = request.form['eid']
			if CheckOwner(eid):
				e = Election.query.filter_by(id=eid).first()
				e.name = request.form['name']
				e.description = request.form['desc']
				db.session.commit()
				flash('Election settings updated')
				return redirect(url_for('election', id=e.id, code=303))
			else:
				flash('You do not own an election by that id')
		return redirect(url_for('index'))
		

# Process votes and present return code. 
@app.route('/vote', methods=['GET', 'POST'])
def vote():
	token = request.args.get('token')
	if request.args.get('action') == 'vote':
		if request.args.get('cid') != None and request.args.get('eid') != None:
			confirmationcode = RegisterVote(request.args.get('cid'), token)
			if  confirmationcode != False:
				e = Election.query.filter_by(id=request.args.get('eid')).first()
				if e.shareurl == 1:
					resulturl = e.resulturl
				else:
					resulturl = ''
				return render_template('voted.html', resulturl=resulturl, confirmationcode=confirmationcode)
			else:
				flash('Your token or vote is invalid.')
		return redirect(url_for('index'))
	else:
		t = Token.query.filter_by(token=token).first()
		if t is not None:
			e = Election.query.filter_by(id=t.election).first()
			if e.status==0:
				admin = User.query.filter_by(id=e.owner).first().email
				return render_template('closed.html', admin=admin)
			else:
				c = GetChoices(e.id)		
				return render_template('vote.html', election=e, choices=c, token=token)
		else:
			flash('Your token is invalid')
			return redirect(url_for('index'))	


# Delete choices for election
@app.route('/choice', methods=['GET', 'POST'])
@login_required
def choice():
	cid = request.args.get('cid')
	eid = request.args.get('eid')
	if CheckOwner(eid):
		if DeleteChoice(eid, cid):
			flash('Choice deleted')
			return redirect(url_for('election', id=eid))
	else:
		flash('Something went wrong')
		return redirect(url_for('election', id=eid))
	return redirect(url_for('election', id=eid))


# Admin users
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
	if current_user.is_admin():
		users = User.query.all()
	else:
		users = User.query.filter_by(username=current_user.username)
	e = GetElections(current_user.username)
	return render_template('admin.html', users=users, elections=e, page='admin')


# Send invites for election
@app.route('/sendinvites', methods=['GET', 'POST'])
@login_required
def sendinvites():
	if request.method=='POST':
		sender = request.form.get('sender')
		message = request.form.get('message')
		subject = request.form.get('subject')
		addresses = request.form.get('addresses')
		eid = request.form.get('eid')
		if sender == '' or message == '' or addresses == '':
			flash('You must fill in all fields')
			return redirect('/sendinvites', id=request.form.get('eid'))
		if not CheckOwner(eid):
			flash('You do not have an election by that ID')
			return redirect(url_for('index'))

		if SendMails(sender, subject, addresses, message, eid, request.base_url.replace('/sendinvites', '') + '/vote?eid='+eid):
			flash('Invites sent!')
			return redirect(url_for('index'))

	eid = request.args.get('id')
	if not CheckOwner(eid):
		flash('You do not have an election by that ID')
		return redirect(url_for('index'))
	else:
		election = Election.query.filter_by(id=eid).first()
		return render_template('sendinvites.html', election=election)


# Update users
@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
	if request.method=='POST':
		if request.form.get('admin', None) is None:
			admin=0
		else:
			admin=1

		# if we have a userid we're updating the user
		if request.form.get('userid', None) is not None:
			if current_user.username == User.query.filter_by(id=request.form.get('userid')).first().username or current_user.is_admin():
				if UpdateUser(request.form['userid'], request.form['username'], request.form['email'], request.form['password'], request.form['passwordconfirm'], admin):
					flash('User ' + request.form['username'] + ' updated')
				else:
					flash('Error updating user ' + request.form['username'])
			else:
				flash('You are not an administrator')
				return redirect(url_for('index'))
		else:
		# if no userid, we're creating a user
			if current_user.is_admin():
				if AddUser(request.form['username'], request.form['email'], request.form['password'], request.form['passwordconfirm'], admin):
					flash('User ' + request.form['username'] + ' added')
				else:
					flash('Error creating user ' + request.form['username'])
			

	if request.method=='GET':
		uid = request.args.get('id')
		user = User.query.filter_by(id=uid).first().username

		if user is not None:
			if current_user.username == user or current_user.is_admin():
				if DeleteUser(uid):
					flash('User ' + user + ' deleted')
				else:
					flash('Error deleting user ' + username)
				
				if current_user.username == user:
					return redirect(url_for('index'))
		else:
				flash('No such user or no permissions')
				return redirect(url_for('index'))
	return redirect(url_for('admin'))			


# Show results page
@app.route('/result', methods=['GET'])
def result():
	token = request.args.get('token')
	e = Election.query.filter_by(resulturl=token).first()
	if e:
		c = GetChoices(e.id)
		r = GetResults(e.id)
		invites = e.invites
		votes = Vote.query.filter_by(election=e.id).count()
		return render_template('result.html', results=r, election=e, choices=c, invites=invites, votes=votes, colors=GetColors(len(c)), result=True)
	else:
		flash('No election found')
		return redirect(url_for('index'))

# Process login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
        	next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Show all submitted values, for debugging only
#@app.route('/test', methods=['GET', 'POST'])
#def test():
#	values = request.form.values()
#	return render_template('test.html', values=values)

# Logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
