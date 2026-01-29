import dataclasses
import datetime
from pathlib import Path
from typing import Optional


# Format season and episode

@dataclasses.dataclass
class EpisodeFormat:
    series: Optional[str] = None
    """Series name"""
    season: Optional[int] = None
    """Season number"""
    episode: Optional[int] = None
    """Episode number"""
    year: Optional[int] = None
    """Production year"""
    title: Optional[str] = None
    """Episode title"""
    season_name: Optional[str] = None
    """Season name"""

    _episode_prefix = 'EP'
    description: Optional[str] = None
    """Episode description"""
    date: Optional[datetime.date] = None
    """Episode date"""

    @staticmethod
    def from_dict(data) -> 'EpisodeFormat':
        ep = EpisodeFormat()
        for key, value in data.items():
            if hasattr(ep, key):
                setattr(ep, key, value)
        return ep

    def series_name(self):
        if self.series is not None:  # Not part of a series
            if self.year is not None:
                return '%s (%d)' % (self.series, self.year)
            else:
                return self.series

        else:
            return self.series

    def season_format(self):
        season = ''
        if self.season_name is not None:  # Named season
            season += '- %s ' % self.season_name

        if season is not None:  # Series has numbered seasons
            self.episode_prefix = 'E'
            season += 'S%02d' % self.season  # Add season number

        return season

    def episode_number(self, episode_name=True):
        name = self.season_format()
        if self.episode is not None:
            name += '%s%02d' % (self.episode_prefix, self.episode)
        if self.title is not None and episode_name:
            if name:  # Append episode title
                return '%s - %s' % (name, self.title)
            else:
                return self.title
        else:
            return name

    def episode_name(self):
        # Prepend series name
        return ('%s %s' % (self.series_name(), self.episode_number())).strip()

    def file_name(self, extension=None) -> Path:
        file = Path(self.episode_name())
        if extension:
            return file.with_suffix(extension)
        else:
            return file

    def folder(self) -> Path:
        return Path('%s %s' % (self.series_name(), self.season_format()))

    def file_path(self, extension: str = '', base_path: Path = None, create_folder=False) -> Path:
        if base_path:
            folder = base_path.joinpath(self.folder())
        else:
            folder = self.folder()

        if create_folder:
            folder.mkdir(exist_ok=True)

        return folder.joinpath(self.file_name(extension))
