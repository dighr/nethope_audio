'''
This python script uses google's transcription and translation API to transcribe and translate audios.
'''

import io
from google.cloud.speech import enums as speech_enums
from google.cloud.speech import types as speech_types
from google.cloud import speech
from google.cloud import translate
from google.cloud import storage
import helpers.utils as util
import helpers.constants as const
import ntpath


# Transcription
# trascribe audios
def transcribe_audio(file_path, language_code):
    duration, new_path, frame_rate, channels = util.pre_process_audio(file_path)
    # Detects speech in the audio file
    if duration < 60:
        response = transcribe_short(new_path, frame_rate, language_code)
    else:
        response = transcribe_large(new_path, frame_rate, language_code)

    return response


# transcribe short audios
def transcribe_short(file_path, frame_rate, language_code):
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(file_path, 'rb') as audio_file:
        # encode
        content = audio_file.read()
        audio = speech_types.RecognitionAudio(content=content)

    config = speech_types.RecognitionConfig(
        encoding=speech_enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=language_code)

    response = client.recognize(config, audio)

    return response


# transcribe large audios
def transcribe_large(full_audio_name, frame_rate, language_code):
    audio_file_name = ntpath.basename(full_audio_name)

    upload_to_bucket(const.TRANSCRIPTION_GOOGLE_BUCKET, full_audio_name, audio_file_name)

    gcs_uri = 'gs://' + const.TRANSCRIPTION_GOOGLE_BUCKET + '/' + audio_file_name

    client = speech.SpeechClient()
    audio = speech_types.RecognitionAudio(uri=gcs_uri)

    config = speech_types.RecognitionConfig(
        encoding=speech_enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=language_code,
            )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=10000)

    delete_from_bucket(const.TRANSCRIPTION_GOOGLE_BUCKET, audio_file_name)
    return response


# upload files to the specified bucket
def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


# upload files to the specified bucket
def read_file_from_bucket(bucket_name, file_name):
    """return  file content in the bucket as string."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(ntpath.basename(file_name))
    return blob.download_as_string()


def delete_from_bucket(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


# Translation
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

