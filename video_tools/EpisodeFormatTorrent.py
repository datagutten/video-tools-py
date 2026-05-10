import copy
from pathlib import Path

import dataclasses
import re

from video_tools import EpisodeFormat


@dataclasses.dataclass
class EpisodeFormatTorrent(EpisodeFormat):
    """
    Generate torrent names
    """
    audio: str = None
    resolution: str = '1080p'
    state: str = None
    """
    Hybrid, repack , proper
    """
    _source: str = None
    source_type: str = None
    _vcodec: str = None

    _acodec: str = 'DD'
    channels: str = '2.0'
    tag: str = None
    _dub: str = None

    def __post_init__(self):
        # _validate_dub(self.dub)
        pass

    @classmethod
    def from_string(cls, epnum: str, **kwargs):
        season, episode = re.search(r'S(\d+)E(\d+)', epnum).groups()
        return cls(season=int(season), episode=int(episode), **kwargs)

    def torrent_format(self):
        # title = '%s %s %s' % (self.series, self.year, self.episode_number())
        if self.remux:
            tags = [self.series, self.year, self.episode_number(), self.state, self.resolution, self.source,
                    self.source_type,
                    self.vcodec,
                    self.dub,
                    self.acodec, self.channels]
        else:
            tags = [self.series, self.year, self.episode_number(), self.state, self.resolution, self.source,
                    self.source_type, self.dub,
                    self.acodec, self.channels, self.vcodec]
        title = ' '.join([str(tag) for tag in tags if tag is not None])
        if self.tag is not None:
            title += '-' + self.tag
        return title

    def episode_name(self):
        return self.torrent_format()

    def folder(self) -> Path:
        temp = copy.deepcopy(self)
        temp.episode = None
        temp.title = None
        return Path(temp.torrent_format())

    def file_name(self, extension=None) -> Path:
        file = Path(self.episode_name())
        if extension:
            return Path(str(file) + extension)
        else:
            return file

    def __str__(self):
        return self.torrent_format()

    # @property
    def _get_vcodec(self):
        return self._vcodec

    # @vcodec.setter
    def _set_vcodec(self, value: str):
        if type(value) is not str:
            return
        value = re.sub(r'MPEG(\d)', r'MPEG-\1', value)

        codecs_disc_remux = ['MPEG-2', 'VC-1', 'AVC', 'HEVC']
        codecs_web_untouched = ['H.264', ' H.265', ' VP9', 'MPEG-2']
        codecs_encode = ['x264', 'x265', 'AV1']
        codecs = codecs_disc_remux + codecs_web_untouched + codecs_encode
        if value not in codecs:
            raise ValueError('Invalid vcodec value')
        self._vcodec = value

    # @property
    def _get_acodec(self):
        return self._acodec

    # @acodec.setter
    def _set_acodec(self, value):
        if not value or type(value) is not str:
            self._acodec = None
            self.channels = None
            return
        codecs = ['DD', 'DD EX', 'DD+', 'DD+ EX', 'TrueHD', 'DTS', 'DTS-ES', 'DTS-HD MA', 'DTS-HD HRA', 'DTS:X', 'LPCM',
                  'FLAC', 'ALAC', 'AAC', 'Opus', 'MP2']
        if value not in codecs:
            raise ValueError('Invalid acodec value')
        self._acodec = value

    # @property
    def _get_dub(self) -> str:
        return self._dub

    # @dub.setter
    def _set_dub(self, value: str | None):
        if not value or type(value) is not str:
            return
        if value not in ['Dual Audio', 'Dubbed', 'MULTI']:
            raise ValueError('Invalid dub value')
        self._dub = value

    @property
    def multi(self):
        return self.dub == 'MULTI'

    @multi.setter
    def multi(self, multi: bool = False):
        if multi:
            self.dub = 'MULTI'

    @property
    def remux(self):
        return self.source == 'REMUX'

    @remux.setter
    def remux(self, remux: bool = False):
        if remux:
            self.source = 'REMUX'
        else:
            self.source = ''

    def _get_source(self):
        return self._source

    def _set_source(self, value: str):
        sources_any = ['3D BluRay', 'BluRay', 'UHD BluRay', 'HDDVD']
        sources_remux = ['NTSC DVD REMUX', 'PAL DVD REMUX']
        sources_encode = ['DVDRip', 'VHSRip']
        # if self.remux and value not in sources_any + sources_remux:
        if self.source and value not in sources_any + sources_remux + sources_encode and 'WEB' not in self.source_type:
            raise ValueError('Invalid source')

        self._source = value

    dub: str = property(_get_dub, _set_dub)
    acodec: str = property(_get_acodec, _set_acodec)
    vcodec: str = property(_get_vcodec, _set_vcodec)
    source: str = property(_get_source, _set_source)
