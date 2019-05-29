#coding: UTF-8
######################################################################################################
#
# API GOOGLE SPEECH TO TEXT
# Módulo de voz para interactuar con el robot, se usa la api de Google speech-to-text.
# Recibe las respuestas de Google, se tratan y se retorna las respuestas clave para interactuar con el robot.
#
# RLP 2019
#
######################################################################################################

from __future__ import division
import re
import sys
from time import sleep
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 5)  # 100ms


class MicrophoneStream(object):

    def __init__(self, rate, chunk):

        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):

        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self


    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()


    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):

        self._buff.put(in_data)
        return None, pyaudio.paContinue


    def generator(self):

        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses, t):
 
    num_chars_printed = 0
    totalChar = 0
    tempTranscript = ""
    for response in responses:
        
        if not response.results:
           
            continue
	result = response.results[0]
        if not result.alternatives:            
            continue

        transcript = result.alternatives[0].transcript
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))
        if " " in tempTranscript:
                if "hexa" in tempTranscript or "EXA" in tempTranscript or "ECSA" in tempTranscript or "Roberto" in tempTranscript:
                    return tempTranscript
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            num_chars_printed = 0

        totalChar += len(transcript)
            
        if totalChar > t:
            return ""            
 
        tempTranscript = transcript


def speech2text(t):
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'es-ES'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        return listen_print_loop(responses, t)
