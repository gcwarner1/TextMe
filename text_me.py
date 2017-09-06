# -*- coding: utf-8 -*- 

'''
This module sends you a text (SMS) when your script finishes and lets you know whether it ran successfully or crashed.
Usage:
	textme = textMe(number=yournumber, carrier=yourcarrier)
	textme.run()

If you do not have a SMTP server on your network (if you are at the Martinos Center you do) you can use your gmail account
by using:
	textme = textMe(number=yournumber, carrier=yourcarrier, gmail=you@gmail.com, password=yourgmailpassword)
	textme.run()

author: Graham Warner
email: gwarner@mgh.harvard.edu
'''

import atexit, os, smtplib, re, sys, __main__

class ExitHooks(object):
    def __init__(self):
        self.exit_code = None
        self.exception = None


    def hook(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler


    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)


    def exc_handler(self, exc_type, exc, *args):
        self.exception = exc


class textMe():
	def __init__(self, number, carrier, gmail=False, password=False):
		self.number = str(number)
		for x in ['-','(',')',' ']:
			if x in self.number:
				self.number = self.number.replace(x,'')
		self.carrier = carrier
		self.gmail = gmail
		self.password = password
		self.hooks = ExitHooks()
		self.hooks.hook()
		self.thisFile = os.path.realpath(__main__.__file__)
		if self.gmail + self.password == 1:
			if self.gmail == False:
				sys.exit('You forgot to enter your gmail address!')
			elif self.password == False:
				sys.exit('You forgot to enter your gmail password!')


	def findCarrier(self):
		if re.search('(verison)|(verizon)',self.carrier, re.IGNORECASE):
			self.ext = '@vtext.com'
		elif re.search('(at&t)|(att)|(atandt)|(at and t)|(at & t)', self.carrier, re.IGNORECASE):
			self.ext = '@mms.att.net'
		elif re.search('(tmobile)|(t-mobile)|(tmobil)|(t-mobil)', self.carrier, re.IGNORECASE):
			self.ext = '@tmomail.net'
		elif re.search('sprint', self.carrier, re.IGNORECASE):
			self.ext = '@page.nextel.com'
		else:
			sys.exit('Carrier '+self.carrier+' not found')


	def sendTxt(self):
		if self.gmail == False and self.password == False:
			try:
				self.server = smtplib.SMTP('localhost')
			except:
				sys.exit('Failed to connect to SMTP server! You do not appear to have a localhost but fear not! You can still send SMS via your gmail account. When calling this module set input "gmail" to your gmail address and "password" to you gmail password.')
		else: 
			self.server = smtplib.SMTP('smtp.gmail.com:587')
			self.server.starttls()
			try:
				self.server.login(self.gmail, self.password)
			except:
				sys.exit('Are your username and password correct? If so, sometimes gmail blocks sign in attemps from third party apps. Try going to this page https://www.google.com/settings/security/lesssecureapps and selecting TURN OFF. If that doesnt work there may be a problem with your ports...¯\_(ツ)_/¯')
		if self.hooks.exit_code == None and self.hooks.exception == None:
			msg = self.thisFile+' ran successfully!'
		else:
			msg = self.thisFile+' crashed!'
		
		if self.gmail == False:
			self.server.sendmail('textMe@script.com', self.number+self.ext, msg)
		else:
			self.server.sendmail(self.gmail, self.number+self.ext, msg)
		self.server.quit()


	def run(self):
		self.findCarrier()
		atexit.register(self.sendTxt)
