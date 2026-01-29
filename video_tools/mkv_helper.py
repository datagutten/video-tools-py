import re
from typing import Optional, List, Dict

import langcodes
from pymkv import MKVFile, MKVTrack


def normalize_track_name(track: MKVTrack):
    tags = []
    if track.track_name is None:
        track.track_name = ''
    if track.language == 'nb':
        track.language = 'no'

    lang_obj_ietf = langcodes.get(track.language_ietf or track.language)

    if track.track_name.find('Dub') == 0:
        tags.append('Dubtitle')
    if re.search(r'[\[(]CC[)\]]', track.track_name) is not None or track.flag_hearing_impaired:
        tags.append('SDH')
        track.flag_hearing_impaired = True
    if re.search(r'[\[(].*?original.*?[)\]]',
                 track.track_name.lower()) is not None or track.flag_original:
        tags.append('Original')
        track.flag_original = True
    if re.search(r'[\[(].*?forced.*?[)\]]', track.track_name.lower()) is not None or track.forced_track:
        tags.append('Forced')
        track.force_track = True
    if track.track_name.lower().find(
            'synstolking') > -1 or track.flag_visual_impaired or 'audio description' in track.track_name.lower():
        tags.append('Audio Description')
        track.flag_visual_impaired = True

    if tags:
        track.track_name = '%s (%s)' % (lang_obj_ietf.display_name(), ' | '.join(tags))
    else:
        track.track_name = lang_obj_ietf.display_name()

    return track


def normalize_track_names(mkv_file: MKVFile):
    for track in mkv_file.tracks:
        if track.track_type == 'video':
            continue
        normalize_track_name(track)


def find_track(mkv_file: MKVFile, track_type: str, language: str) -> Optional[MKVTrack]:
    for track in mkv_file.tracks:  # TODO: check properties (audio description)
        if track.track_type == track_type and track.language == language:
            return track
    return None


def find_languages(mkv: MKVFile) -> Dict[str, List[str]]:
    """
    Find all languages by track type
    :param mkv: MKV file to search
    :return:
    """
    languages = {}
    track: MKVTrack

    for track in mkv.tracks:
        if track.language == 'und' or not track.language:
            continue
        if track.track_type not in languages:
            languages[track.track_type] = [track.language]
        else:
            languages[track.track_type].append(track.language)

    return languages


def find_subtitles(mkv: MKVFile) -> List[MKVTrack]:
    """
    Find all subtitle tracks
    :param mkv: MKV file to search
    :return: List of subtitle tracks
    """
    tracks = []
    for track in mkv.tracks:
        if track.track_type == 'subtitles':
            tracks.append(track)
    return tracks
