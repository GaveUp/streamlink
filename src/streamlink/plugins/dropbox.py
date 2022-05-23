"""
$description Global file hosting platform.
$url dropbox.com
$type vod
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r"https://(?:www\.)dropbox\.com/s/[^/]"
))
class Dropbox(Plugin):
    m3u8_re = re.compile(r'''"transcode_url"\s*:\s*"(.*?)"''')

    config_schema = validate.Schema(
        validate.transform(m3u8_re.search),
        validate.any(None,
                     validate.all(
                         validate.get(1)
                     ))
    )

    def _get_streams(self):
        data = self.session.http.get(self.url, schema=self.config_schema)

        return HLSStream.parse_variant_playlist(self.session, data)


__plugin__ = Dropbox
