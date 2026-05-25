from pathlib import Path

import m3u8
from pymkv import MKVFile


def mkv_track_flags_args_from_m3u8(media: m3u8.Media):
    """
    Get MKV track flags from m3u8 attributes
    :param media: m3u8 media object
    :return: Dict with pymkv.Track arguments
    """
    if media.characteristics:
        characteristics = media.characteristics.split(',')
    else:
        characteristics = []
    flags = {
        'track_name': media.name,
        'language_ietf': media.language,
        'default_track': media.autoselect == 'YES',
        'forced_track': media.forced == 'YES',
        'flag_hearing_impaired': 'public.accessibility.describes-music-and-sound' in characteristics,
        # 'flag_original': media.characteristics == 'public.accessibility.transcribes-spoken-dialog',
        'flag_visual_impaired': 'public.accessibility.describes-video' in characteristics,
    }
    if media.type == 'AUDIO':
        del flags['forced_track']
    return flags


def mkv_track_flags_m3u8(mkv: MKVFile, m3u8_file: Path):
    """
    Set track flags for all tracks in an MKV file based on tracks with the name in a m3u8 file
    """
    m3u8_data = m3u8.loads(m3u8_file.read_text(encoding="utf-8"))
    m3u8_tracks = {}
    for track in m3u8_data.media:
        if track.type not in m3u8_tracks:
            m3u8_tracks[track.type] = {}
        m3u8_tracks[track.type][track.name] = track

    for track in mkv.tracks:
        if track.track_type == 'video':
            continue
        m3u8_track = m3u8_tracks[track.track_type.upper()][track.track_name]
        args = mkv_track_flags_args_from_m3u8(m3u8_track)
        for arg, value in args.items():
            setattr(track, arg, value)
