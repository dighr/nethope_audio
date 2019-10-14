'''
This python class uses google's transcription and translation API to transcribe audios.
There are different methods within this class to translate and get sentiment values of texts
To use this class, ensure that the "" is within the environment
'''

import os
import io
from google.cloud.speech import enums as speech_enums
from google.cloud.speech import types as speech_types
from google.cloud import speech
from multiprocessing.dummy import Pool
import speech_recognition as sr
from pydub import AudioSegment
from google.cloud import language
from google.cloud import translate
from google.cloud.language import enums
from google.cloud.language import types


tmp_path = os.path.join('.', 'tmp')


def translate_text_from(text, source_language, target_language="en"):
    client = translate.Client()
    translation = client.translate(text,
                                   source_language=source_language, target_language=target_language)
    response = {
        'source_language': source_language,
        'text': text,
        'translation': translation['translatedText'],
    }

    return response


# translates text from any language to any target language with all the languages supported by
# google's API
def translate_text_from(text, source_language, target_language="en"):
    client = translate.Client()
    translation = client.translate(text,
                                   source_language=source_language, target_language=target_language)

    print(translation)

    return translation['translatedText']


# Get text's sentiment values and extract entities
def get_text_sentiment_values(text):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    features = {
        "extract_entities": True,
        "extract_document_sentiment": True,
        "extract_entity_sentiment": True,
    }

    result = client.annotate_text(document=document, features=features)

    return result


# trascribe audios less than one minute with wav format
def transcribe_short_audio(file_path, language_code):
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(file_path, 'rb') as audio_file:
        # encode
        content = encode_audio(audio_file)
        audio = speech_types.RecognitionAudio(content=content)

    config = speech_types.RecognitionConfig(
        encoding=speech_enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code)

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    text = ""
    for result in response.results:
        text += result.alternatives[0].transcript

    return text


# Transcribe audio with any length, the way this is done is by first, dividing the audio file into smalled chucks
# of 45 seconds, each chuck is transcribed in a separate thread and then assembled in an ordered way at the end
def transcribe_audio_fast(file_path, language_code, name="tmp"):
    # Since tmp_file is required, create it if it does not exist
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    # Open google APPLICATION CREDENTIALS which is stored in the enviroment variables
    with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]) as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    sound = AudioSegment.from_wav(file_path)

    r = sr.Recognizer()

    # initialize data
    data = []

    # Calculate the voice chucks in miliseconds in the following format (chuck_begin, chuck_end)
    # Append this into the data list
    duration = sound.duration_seconds * 1000
    interval = 58 * 1000
    begin = 0
    if interval < duration:
        end = interval
    else:
        end = duration

    while duration > 0:
        data.append((begin, end))

        # update
        duration -= interval
        begin = end
        if duration < interval:
            end = (end + duration)
        else:
            end = (end + interval)

    # This inner method will be run in a separate thread
    def transcribe(input):
        import binascii
        idx, value = input
        # Retreive the chunck from the audio and store it in the tmp file with a unique name
        sound_interval = sound[value[0]:value[1]]
        audio_segment_path = os.path.join(tmp_path, name + str(binascii.hexlify(os.urandom(32)).decode()) + ".wav")

        out = sound_interval.export(audio_segment_path, format="wav")

        # with sr.AudioFile(audio_segment_path) as source:
        #     audio = r.record(source)

        # Transcribe audio file
        try:
            text = transcribe_short_audio(audio_segment_path, language_code)
        except sr.UnknownValueError:
            text = "*********sub audio was not understood*********"

        # Clear
        os.remove(audio_segment_path)
        out.close()

        return {
            "idx": idx,
            "text": text
        }

    pool = Pool(20)
    all_text = pool.map(transcribe, enumerate(data))
    pool.close()
    pool.join()

    transcript = ""
    for t in sorted(all_text, key=lambda x: x['idx']):
        # Format time as h:m:s - 30 seconds of text
        transcript += t['text']

    return transcript


# Encode the audio function
def encode_audio(audio):
    audio_content = audio.read()
    # return base64.b64encode(audio_content)
    return audio_content


class GoogleTranscription:
    def __init__(self, language_code):
        self.language_code = language_code

    def transcribe(self, file_name):
        sound = AudioSegment.from_wav(file_name)
        duration = sound.duration_seconds

        # Based on the duration, transcribe the audio files
        if duration < 60:
            text = transcribe_short_audio(file_name, self.language_code)
        else:
            text = transcribe_audio_fast(file_name, self.language_code)

        return text
