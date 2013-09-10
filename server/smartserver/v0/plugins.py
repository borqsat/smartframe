#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from bottle import PluginError, request
import inspect

__all__ = ["err", "ContentTypePlugin", "LoginPlugin"]


def err(code='500', msg='Unknown error!'):
    """
    generate error message.
    """
    return {'errors': {'code': code, 'msg': msg}}


# Plugin to check if the request has a content-type not in *types.
# if no, then return error message.
class ContentTypePlugin(object):
    '''This plugin checks the content-type of the request'''
    name = 'content-type'
    api = 2

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, ContentTypePlugin):
                continue
            raise PluginError("Found another Content-Type plugin with "
                              "conflicting settings (non-unique keyword).")

    def apply(self, callback, route):
        contenttypes = route.config.get('content_type', [])
        if not isinstance(contenttypes, list):
            contenttypes = [contenttypes]

        if len(contenttypes) is 0:
            return callback  # content-type not specified

        def wrapper(*args, **kwargs):
            for t in contenttypes:
                if t.lower() in request.content_type:
                    return callback(*args, **kwargs)

            return err(code='500', msg='Invalid content-type header!')

        return wrapper


# Plugin to check if the request contrains a valid token. The token param may be in query, form or json
# If yes, put the uid in the **kwargs
class LoginPlugin(object):
    '''This plugin gets the token param in query string or json body, and check if the token is valid.
    If yes, pass the token or uid to the callback keywords, depending on the original callback accepts
    'uid' or 'token' keyword. '''
    name = 'login'
    api = 2

    def __init__(self, getuserid, request_token_param="token", login=True, token_keyword="token", uid_keyword="uid"):
        self.getuserid = getuserid
        self.login = login
        self.request_token_param = request_token_param
        self.token_keyword = token_keyword
        self.uid_keyword = uid_keyword

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, LoginPlugin):
                continue
            raise PluginError("Found another login plugin with "
                              "conflicting settings (non-unique keyword).")

    def apply(self, callback, route):
        # Test if the original callback accepts a 'uid' or 'token' keyword.
        args = inspect.getargspec(route.callback)[0]
        has_uid = self.uid_keyword in args
        has_token = self.token_keyword in args
        # return original callback if login is False
        login = route.config.get('login', self.login)
        # if login=False and callback don't has 'uid' and 'token' keyword,
        # don't check whether the token is logined.
        if not (login or has_uid or has_token):
            return callback

        def wrapper(*args, **kwargs):
            uid = None
            if request.params and self.request_token_param in request.params:
                # get token from params and then get uid
                token = request.params[self.request_token_param]
                uid = self.getuserid(token)
            elif request.json and self.request_token_param in request.json:
                # get token from request.json and then get uid
                token = request.json[self.request_token_param]
                uid = self.getuserid(token)
            elif request.get_header("X-%s" % self.request_token_param) is not None:
                token = request.get_header("X-%s" % self.request_token_param)
                uid = self.getuserid(token)
            else:
                # No token param.
                return err('03', 'The API needs a valid "token" parameter. No token provided in the request!')

            if uid is None:  # if the uid is None, then we return an error message.
                return err('01', 'Invalid token!')
            else:  # pass uid/token to callback
                if has_uid:
                    kwargs[self.uid_keyword] = uid
                if has_token:
                    kwargs[self.token_keyword] = token
                return callback(*args, **kwargs)

        # Replace the route callback with the wrapped one.
        return wrapper
