import os
import random
from pydub import AudioSegment
from pydub.utils import mediainfo

def get_song_metadata(filepath):
    info = mediainfo(filepath)
    title = info.get("TAG", {}).get("title", os.path.basename(filepath).split('.')[0])
    duration_ms = int(float(info.get("duration", 0)) * 1000)
    return title, duration_ms

def apply_pro_transition(outgoing, incoming, overlap_ms):
    # Your filtering logic remains here
    out_mid_high = outgoing.high_pass_filter(1300).fade_out(overlap_ms)
    in_bass_intro = incoming.low_pass_filter(1000).fade_in(overlap_ms)
    out_ducked = out_mid_high - 3.0 
    return out_ducked.overlay(in_bass_intro, gain_during_overlay=2.5)
def apply_echo_out(audio_seg, delay_ms=1000, decay_db=8):
    """Applies a professional echo/delay effect to the very end of the mix."""
    tail = audio_seg[-2000:]
    echo = tail.overlay(tail - decay_db, position=delay_ms).overlay(tail - (decay_db*2), position=delay_ms*2)
    return audio_seg[:-2000] + echo.fade_out(2000)

def process_mixtape(audio_files, output_path, transition_ms=8000):
    mixtape = None
    tracklist_data = []
    
    for file_path in audio_files:
        song_name, duration = get_song_metadata(file_path)
        song = AudioSegment.from_file(file_path).set_channels(2).set_frame_rate(44100).normalize()

        if mixtape is None:
            mixtape = song
            tracklist_data.append({"name": song_name, "duration": duration, "overlap": 0})
        else:
            overlap = min(transition_ms, len(song) // 3, len(mixtape) // 3)
            bridge = apply_pro_transition(mixtape[-overlap:], song[:overlap], overlap)
            mixtape = mixtape[:-overlap] + bridge + song[overlap:]
            tracklist_data[-1]["overlap"] = overlap
            tracklist_data.append({"name": song_name, "duration": duration, "overlap": 0})
    # Apply Final Echo Out to the very end of the mixtape
    mixtape = apply_echo_out(mixtape)

    mixtape.export(output_path, format="mp3", bitrate="320k")
    return tracklist_data