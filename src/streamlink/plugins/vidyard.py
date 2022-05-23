"""
$description Global video hosting platform.
$url vidyard.com
$type vod
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https://share\.vidyard\.com/watch/(.+)[^/]"
))
class Vidyard(Plugin):
    api_url = "https://play.vidyard.com/player/{0}.json"

    config_schema = validate.Schema(
        validate.any(None,
                     validate.all(
                         validate.parse_json(),
                         validate.get("payload"),
                         validate.get("chapters"),
                         validate.get(0),
                         validate.get("sources"),
                         validate.get("hls"),
                         [{
                             "profile": validate.text,
                             "url": validate.url()
                         }]
                     ))
    )

    def _get_streams(self):
        vidid = self.match.group(1)
        log.debug("Vidyard Video ID: {0}".format(vidid))
        data = self.session.http.get(self.api_url.format(vidid), schema=self.config_schema)

        for info in data:
            if info["profile"] == "auto":
                return HLSStream.parse_variant_playlist(self.session, info["url"], headers={"Referer": self.url})


__plugin__ = Vidyard
