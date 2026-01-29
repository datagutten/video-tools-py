import re
from pathlib import Path


def find_episodes(path: Path, extensions=None) -> dict[str, Path]:
    """
    Find all episodes in the given path and all subdirs
    """
    episodes = {}
    for episode in path.iterdir():
        if episode.is_dir():
            episodes.update(find_episodes(episode))
        else:
            matches = re.search(r'(S\d+E\d+)', episode.name)
            if not matches:
                continue
            if extensions is not None and episode.suffix not in extensions:
                continue
            episodes[matches.group(1)] = episode
    return episodes


def parse_episode(episode_str: str):
    matches = re.search(r'S(\d+)E(\d+)', episode_str)
    return int(matches.group(1)), int(matches.group(2))
