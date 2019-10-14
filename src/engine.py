import re
import time
import src.google_transcription as gt


# For the given name NO extension, extract the timestamp portion and store it in epoch format
# The given name comes in a similar format to the following 0c20191010155022n7879579094_0.amr
def extract_info_from_name(name):
    # Check if format is valid
    pattern = re.compile('0c[0-9]{14}n[0-9]{10}_0')
    if not pattern.match(name):
        raise Exception('name does not stick to the format of "0c[0-9]{14}n[0-9]{10}_0"'.format(name))

    # For each file, extract the timestamp portion and store it in epoch format
    date_time = re.findall('[0-9]{14}', name)[0]
    pattern = '%Y%m%d%H%M%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    # The audio file’s timestamp is stored in local time, which is UTC-4, so we need to add (4*60*60*1000)=14,400,000
    epoch += (4 * 60 * 60 * 1000)
    # Extract the phone number from name
    phone_num = re.findall('[0-9]{10}_', name)[0].replace('_', '')
    # Return epoche and phone number
    return epoch, phone_num


# Transcribe and then translate the audio
def transcribe_and_translate(file_loc, source_lang_code, target_lang_code):
    gt_obj = gt.GoogleTranscription(source_lang_code)
    transcription = gt_obj.transcribe(file_loc)
    print(transcription)
    translation = gt.translate_text_from(transcription, source_lang_code.split("-")[0], 'ar')
    return transcription, translation

# Store the given params into the db
def store_in_db(epoche, phone_num, transcription, translation):
    pass


print(transcribe_and_translate('../data/example.wav', 'en', 'ar'))


