import os

SUPPORTED_AUDIO_ENCODING = ['wav', 'mp3', 'amr', '.wav', '.mp3', '.amr']
TRANSCRIPTION_GOOGLE_BUCKET = 'long_audios_trans'
AUDIOS_TRANSCRIPTION = 'audios-transcriptions'
AUDIOS_TRANSLATION = 'audios-translation'
DropBox_API_KEY = os.environ["DropBox_API_KEY"]
DOWNLOAD_PATH = './Downloads/'
