#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The auth via trust pop3 server for Django http://www.djangoproject.com
set up the trust pop3 server domain in AUTH_POP_SERVERS, you could have one or many
trusted pop3 server

require python package python-dnspython, http://www.dnspython.org/
for smart MX record lookup

ex:

POP3_AUTH_SERVERS = {'companydomain1.com':'com1','companydomain2.com':'com2'}

"""
import string
import poplib
import socket
from django.contrib.auth.models import User
import dns.resolver
from django.conf import settings
import re
import logging

POP3_AUTH_SERVERS, POP3_BAD_USERS = settings.POP3_AUTH_SERVERS, settings.POP3_BAD_USERS

email_re = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

logger = logging.getLogger(__name__)

class POP3Backend:

    def auth_pop3_server(self, email=None, password=None):
        # find mailserver first
        domain = ''
        username = ''
        ms = '' # mail server

        if email_re.search(email):
            logger.debug("regular expression matched.")
            print 're matched'
            username = email[:email.find('@')]
            domain = email[email.find('@')+1:]

        if username and domain in POP3_AUTH_SERVERS.keys():
            logger.debug("POP3 server config found.")
            print 'pop3 server config found'
            # find domain name
            if username in POP3_BAD_USERS:
                logger.error('bad user :(')
                return False

            try:
                # trim the last dot character
                ms= POP3_AUTH_SERVERS[domain]

                # pop3 ssl fail, let's try pop
                m = poplib.POP3(ms)
                m.user(username)
                m.pass_(password)
                if m.stat():
                    return True
                else:
                    return False

            except:
                # some error
                return False

        return False

    def authenticate(self, username=None, password=None):
        # Authenticate the base user, the username is an email address
        # If the user does not exist in POP3 server, Fail.
 
        if not self.auth_pop3_server(email=username, password=password):
            return None

        try:
            user = User.objects.get(email=username)
        except:
            from random import choice
            temp_pass = ""
            new_user = ''
            domain = ''
            if email_re.search(username):
                domain = username[username.find('@')+1:]
                new_user = username[:username.find('@')]
                new_user = new_user + '_' +POP3_AUTH_SERVERS[domain]
                new_user = string.lower(new_user)
            for i in range(8):
                temp_pass = temp_pass + choice(string.letters)
            user = User.objects.create_user(new_user, username, temp_pass)
            user.is_staff = False
            user.save()

        # Success.
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
