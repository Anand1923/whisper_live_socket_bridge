from whisper_live.client import TranscriptionClient

client = TranscriptionClient(
    host="localhost",
    port=9090,
    lang="en",
    translate=False,
    model="medium",  # Optional if server uses default
    use_vad=True,    # Uses voice activity detection
    max_connection_time=600,
)

client()