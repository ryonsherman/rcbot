#!/usr/bin/env python2


class Command:
    def __init__(self, *args, **kwargs):
        self.client = kwargs['client']
        self.user = kwargs['user']
        self.channel = kwargs.get('channel', None)
        self.args = kwargs.get('args', [])

    def message(self, message, user=None):
        if self.channel:
            self.client.messageChannel(self.channel, message, user)
        else:
            user = self.user if not user else user
            self.client.messageUser(user, message)
