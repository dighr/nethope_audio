from pydub import AudioSegment
import wave
import ntpath
import src.constants as const


def convert_to_wav(audio_file_name):
    extension = ntpath.basename(audio_file_name).split('.')[-1]

    if extension not in const.SUPPORTED_AUDIO_ENCODING:
        raise Exception(extension + 'is not supported')

    file_name_without_extension = ntpath.basename(audio_file_name).split('.')[0]
    if extension == 'wav':
        sound = AudioSegment.from_wav(audio_file_name)
        return sound.duration_seconds, audio_file_name

    elif extension == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)

    # AMR at this point
    else:
        sound = AudioSegment.from_file(audio_file_name, format='amr')

    sound.export(audio_file_name, format="wav")
    duration = sound.duration_seconds

    return duration, ntpath.dirname(audio_file_name).join((file_name_without_extension + '.wav'))


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
        text += result.alternatives[0].transcript + '\n'

    return text


def pre_process_audio(full_audio_name):
    # preprocess
    duration, path = convert_to_wav(full_audio_name)
    frame_rate, channels = frame_rate_channel(full_audio_name)
    if channels > 1:
        stereo_to_mono(full_audio_name)

    return duration, path, frame_rate, channels
