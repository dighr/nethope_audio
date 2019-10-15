
import src.engine as engine
transcription, translation = engine.transcribe_and_translate('../data/example2.wav', 'en', 'ar')
print(transcription)
print(translation)