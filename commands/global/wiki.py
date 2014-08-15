#!/usr/bin/env python2

import re
import json
import urllib

from xml.etree import ElementTree

from utils.text import style
from commands import Command

pattern = re.compile(ur"#<p>(.*)</p>#Us")


class wiki(Command):
    syntax = "Syntax %s %s" % (
        style.bold("!wiki"), 
        style.underline("phrase"))

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        if not self.args:
            return self.message(self.syntax, self.user)

        query = ' '.join(self.args)
        url = "http://en.wikipedia.org/w/api.php?format=json&action=query&%s&prop=revisions&rvprop=content" % urllib.urlencode({'titles': query})
        results = json.loads(urllib.urlopen(url).read())['query']

        if not results.get('pages', False): return
        page = results['pages'].popitem()[1]
        title = page['title']

        if not page.get('pageid', False): 
            return self.message("No Wikipedia page for \"%s\"" % query, self.user)

        url = "http://en.wikipedia.org/w/api.php?action=query&prop=info&pageids=%s&inprop=url&format=xml" % page['pageid']
        xml = ElementTree.fromstring(urllib.urlopen(url).read())
        url = xml.findall(".//page[1]")[0].get('fullurl')

        # TODO: return first paragraph

        self.message("%s (%s)" % (title, url), self.user)
