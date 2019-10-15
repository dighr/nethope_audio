import src.engine as engine

epoche, phone_num = engine.extract_info_from_name("0c20191010155022n7879579094_0")
print(epoche, phone_num)

transcription, translation = engine.transcribe_and_translate('../data/examplewav.wav', 'en', 'ar')
print(transcription)
print(translation)