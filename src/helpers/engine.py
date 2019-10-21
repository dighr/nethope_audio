import re
import time
import src.google_service as gs
import src.utils as util


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
def transcribe_and_translate(file_name, source_lang_code, target_lang_code):
    transcription = gs.transcribe_audio(file_name, source_lang_code)
    text = util.transcript_response_to_paragraph(transcription)
    translation = gs.translate_text_from(text, source_lang_code.split("-")[0], target_lang_code)
    return transcription, translation

# TODO Store the given params into the db
def store_in_db(epoche, phone_num, transcription, translation):
    pass