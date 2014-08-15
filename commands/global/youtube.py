#!/usr/bin/env python2

import json
import urllib
import datetime

from gdata.youtube import service

from utils.text import style
from commands import Command


class youtube(Command):
    syntax = "Syntax %s %s" % (
        style.bold("!youtube"), 
        style.underline("phrase"))

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        if not self.args:
            return self.message(self.syntax, self.user)            
        
        query = service.YouTubeVideoQuery()
        query.vq = ' '.join(self.args)
        feed = service.YouTubeService().YouTubeQuery(query)

        if not feed.entry:
            return self.message("No YouTube results for \"%s\"" % query.vq, self.user)

        video = feed.entry[0].media
        title = video.title.text
        duration = datetime.timedelta(seconds=int(video.duration.seconds))
        url = video.player.url.split('&')[0]
        self.message("%s [%s] (%s)" % (title, duration, url), self.user)
