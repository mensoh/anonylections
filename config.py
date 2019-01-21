import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	MAIL_SERVER = 'your.mailserver.com'
	MAIL_DEFAULT_SENDER = 'noreply@noreply.com'
	MAIL_DEBUG = True
