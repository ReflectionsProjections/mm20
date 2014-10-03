#!bin/env/python
import os
from time import sleep

# Pexpect/Fexpect aren't on PYTHONPATH by default, so add it here everytime we run the script
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages') # Pexpect
sys.path.append('/usr/local/lib/python2.7/site-packages/ilogue') # Fexpect
import pexpect # Requires 'pexpect' to auth through SSH

# Config
passwordFile = os.path.abspath("mm20-passwords.txt");

# --- DO NOT MODIFY BELOW ---

# Read auth details
usernames = []
passwords = []

# Push a user's code
def push(username, password):
	url = "http://bitbucket.org/%s/mm20" % username

	# Command
	cmd = 'git push ' + url + ' competitors'

	try:
		p = pexpect.spawn(cmd)

		# Username
		p.expect("Username for 'https://bitbucket.org': ")
		p.send(username)
		p.sendcontrol('m')

		# Password
		p.expect("Password for 'https://%s@bitbucket.org': " % username)
		p.send(password)
		p.sendcontrol('m')

		# Wait for push
		sleep(5)
		p.sendcontrol('m')
		p.close()

		# Done!
		out = p.after
		print out
		p.close()
		sleep(3)

		print "SUCCESS " + username
	except Exception, e:
		print e
		print "FAIL " + username

# Read usernames/passwords from file
usernames =[]
passwords = []

with open(passwordFile) as f:
	for line in f.readlines():
		if len(line) < 5:
			continue
		usernames.append(line.split(" ")[0])
		passwords.append(line.split(" ")[1])

# Push to everyone's Bitbucket (master branch) from current dir
for i in range(1, len(usernames)):
	push(usernames[i], passwords[i])
