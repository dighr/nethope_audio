from pydub import AudioSegment
import wave
import ntpath
import re
import time
import helpers.constants as const
# from google.appengine.ext import ndb


# For the given name NO extension, extract the timestamp portion and store it in epoch format
# The given name comes in a similar format to the following 0c20191010155022n7879579094_0.amr
def extract_info_from_name(name):
    # Check if format is valid
    pattern = re.compile('0c[0-9]{14}n[0-9]{10}_0')
    if not pattern.match(name):
        # raise Exception('name does not stick to the format of "0c[0-9]{14}n[0-9]{10}_0"'.format(name))
        return '', ''
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


def convert_to_wav(audio_file_name):
    extension = ntpath.basename(audio_file_name).split('.')[-1]

    if extension not in const.SUPPORTED_AUDIO_ENCODING:
        raise Exception(extension + 'is not supported')

    # file_name_without_extension = ntpath.basename(audio_file_name).split('.')[0]
    # if extension == 'wav':
    #     sound = AudioSegment.from_wav(audio_file_name)
    #     return sound.duration_seconds, audio_file_name
    #
    # elif extension == 'mp3':
    #     sound = AudioSegment.from_mp3(audio_file_name)
    #
    # # AMR at this point
    # else:
    sound = AudioSegment.from_file(audio_file_name)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_sample_width(2)
    sound.export('./tmp/output.wav', format="wav")
    duration = sound.duration_seconds

    return duration, './tmp/output.wav'


# the input file name has to be a  wav audio file
def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels


def transcript_response_to_paragraph(response):
    text = ''
    for result in response.results:
        text += result.alternatives[0].transcript.encode('utf-16').decode('utf-16') + '\n'

    return text


def pre_process_audio(full_audio_name):
    # preprocess
    duration, path = convert_to_wav(full_audio_name)
    frame_rate, channels = frame_rate_channel(path)
    if channels > 1:
        stereo_to_mono(path)

    return duration, path, frame_rate, channels


def get_transcript(response):
    res = []
    for result in response.results:
        res.append(result.alternatives[0].transcript.encode('utf-16').decode('utf-16'))
    return res
