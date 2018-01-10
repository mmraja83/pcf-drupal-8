"""Key Extension

Generate a pair of keys to encrypt the tokens.
"""
import os
import os.path
import logging
from build_pack_utils import utils

_log = logging.getLogger('oauth')


def preprocess_commands(ctx):
    commands = [
        [ 'openssl genrsa -out /home/vcap/app/cert/private.key 2048'],
        [ 'openssl rsa -in /home/vcap/app/cert/private.key -pubout > /home/vcap/app/cert/public.key'],
        [ 'chmod 600 /home/vcap/app/cert/*']
    ]
    return commands

def service_commands(ctx):
    return {}

def service_environment(ctx):
    return {}

def compile(install):
    print 'Generate keys pair...'
    return 0
