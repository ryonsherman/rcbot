#!/usr/bin/env python2

import json
import urllib

from HTMLParser import HTMLParser

from utils.text import style
from commands import Command


class google(Command):
    syntax = "Syntax %s %s" % (
        style.bold("!google"), 
        style.underline("phrase"))

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        if not self.args:
            return self.message(self.syntax, self.user)
        
        query = ' '.join(self.args)
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % urllib.urlencode({'q': query})
        results = json.loads(urllib.urlopen(url).read())['responseData']['results']

        if not results:
            return self.message("No Google results for \"%s\"" % query, self.user)
        
        result = results[0]
        title = HTMLParser().unescape(result['titleNoFormatting'])[:-4].strip()
        url = result['unescapedUrl'].rstrip('/')
        self.message("%s (%s)" % (title, url), self.user)
