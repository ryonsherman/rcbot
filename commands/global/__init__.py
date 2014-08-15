#!/usr/bin/env python2

import re
import urllib

from BeautifulSoup import BeautifulSoup

from utils import url_pattern
from commands import Command

class Global(Command):
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.parseURL(self.args)

    def parseURL(self, args):
        for arg in args:
            for url in url_pattern.findall(arg):
                if not url.startswith('http'):
                    url = "http://" + url
                title = BeautifulSoup(urllib.urlopen(url),
                    convertEntities=BeautifulSoup.HTML_ENTITIES).title.string.strip()
                self.message("Title: %s (%s)" % (re.sub('\s+', ' ', title), url))
