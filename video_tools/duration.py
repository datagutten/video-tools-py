import os
import re
import subprocess
from pathlib import Path


def check_duration(actual: int | float, expected: int | float, tolerance: int = 90) -> bool:
    """
    Check if the given duration is within the given tolerance
    :param actual: Actual duration
    :param expected: Expected duration
    :param tolerance: Duration tolerance
    :return: Return true is duration is within tolerance
    """
    if expected == actual:
        return True
    diff = abs(actual - expected)
    return diff <= tolerance


def duration_ffprobe(file: Path | str) -> int:
    """
    Get video duration in seconds using ffprobe
    :param file: Video file
    :return: Duration in seconds
    """
    process = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-i', str(file)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.check_returncode()
    matches = re.search(rb'duration=([0-9:.]+)', process.stdout)
    duration = int(float(matches.group(1).decode()))
    return duration


def check_file_duration(file: Path | str, expected: int | float, tolerance: int = 90, rename: bool = True):
    """
    Check if the given file is within the given tolerance and optionally rename the file if it is outside the tolerance
    :param file: File to check
    :param expected: Expected duration
    :param tolerance: Duration tolerance
    :param rename:
    :return:
    """
    file = str(file)
    if not os.path.exists(file):
        raise FileNotFoundError(file)
    # TODO: Check if size is 0
    duration = duration_ffprobe(file)
    duration_check = check_duration(duration, expected, tolerance)
    if not duration_check and rename:
        os.rename(file, file + '_wrong_duration')
    return duration_check
