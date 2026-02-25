import datetime


def generate_youtube_metadata(tracklist_data):
    """
    Creates a title and a description with clickable timestamps.
    """
    year = datetime.date.today().year
    title = f"Seamless AI Mixtape {year} | High-Fidelity Audio Mix"

    description = [
        "🚀 Professional Mix generated with Python Automation.",
        "📌 TRACKLIST (Click timestamps to skip):",
        "",
    ]

    current_time_ms = 0
    for song in tracklist_data:
        # Convert milliseconds to HH:MM:SS format
        seconds = current_time_ms // 1000
        timestamp = str(datetime.timedelta(seconds=seconds)).zfill(8)[3:]

        description.append(f"{timestamp} - {song['name']}")

        # Advance the clock: (Length of song - the time it overlapped with the next)
        current_time_ms += song["duration"] - song["overlap"]
    description.append("\n ✨ HIGHLIGHTS")
    description.append("\n- Smooth 6-second crossfades using high-pass/low-pass filtering.")
    description.append("\n- 320kbps High-Fidelity audio quality.")
    description.append("\n- Curated for a consistent BPM flow.")
    

    description.append("\n#DJMix #PythonAutomation #YouTubeChapters")
    return title, "\n".join(description)
