#!/usr/bin/env python2


class style:
    @staticmethod
    def bold(text):
        return "\x02%s\x02" % text

    @staticmethod
    def underline(text):
        return "\x1F%s\x1F" % text
