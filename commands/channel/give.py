#!/usr/bin/env python2

from utils.text import style
from commands import Command


class give(Command):
    syntax = "Syntax %s %s %s [args]" % (
        style.bold("!give"), 
        style.underline("nickname"), 
        style.underline("command"))

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        if len(self.args) < 2:
            return self.message(self.syntax, self.user)

        user = self.args.pop(0)
        command = self.args.pop(0)

        self.client.parseChannelMessage(
            user, self.channel, '!%s %s' % (command, ' '.join(self.args)))
