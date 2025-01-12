
import time

from queue import Queue
from openai import OpenAI
import speech_recognition as sr


class SpeechToText:

    # time in seconds before recording callback is run again
    record_time_limit = 2

    # time in seconds between recording before a newline is added
    time_to_talk = 3

    def __init__(self, model_task='transcribe'):
        self.data = Queue()

        # create the audio recorder object
        # used for detecting speech only when audio is detected
        self.r = sr.Recognizer()
        self.r.energy_threshold = 1000
        with sr.Microphone() as source:
            print("testing ambient noise levels for 1 second")
            self.r.adjust_for_ambient_noise(source)
            print("done ambient noise adjust")
        # optionally switch above with self.r.energy_threshold = 1000

        # used to stop the recorder from adjusting energy levels while in use
        self.r.dynamic_energy_threshold = False

        # whisper will only read sample rates of 16kHz so our sample rate,
        # should be the same to avoid ffmpeg having to change anything
        self.source = sr.Microphone(sample_rate=16000)

        # requires that OPENAI_API_KEY is defined as environmental variable with openai license
        self.model = OpenAI()
        self.transcription = ['']

    def r_callback(self, _, audio_data):
        """
        Function to be called by speechrecognizer that will add wav data to the queue
        in a separate thread
        :param _:
        :param audio_data: stores a speech_recognition.AudioData instance
        :return: None
        """
        wav_data = audio_data.get_wav_data()
        self.data.put(wav_data)

    def transcribe(self):
        self.r.listen_in_background(self.source, self.r_callback, phrase_time_limit=SpeechToText.record_time_limit)
        time_talking = time.time()
        done_talking = False
        printed_index = 0
        self.transcription = ['']

        print("beginning transcription")
        while True:
            try:
                now = time.time()
                if not self.data.empty():

                    # set done talking to true if more than time to talk seconds passed
                    done_talking = (now - time_talking > SpeechToText.time_to_talk)
                    time_talking = now

                    # concat all binary data in the queue and empty the queue
                    audio_data = b''.join(self.data.queue)
                    self.data.queue.clear()

                    with open("audio_data.wav", 'wb') as f:
                        f.write(audio_data)

                    with open("audio_data.wav", 'rb') as f:
                        result = self.model.audio.transcriptions.create(file=f, model="whisper-1")

                    # store transcription and clean it up
                    text = result.text.strip()

                    if done_talking:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text

                    for i in range(len(self.transcription)):
                        if i >= printed_index:
                            print(self.transcription[i])
                            printed_index += 1
                else:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                for line in self.transcription:
                    print(line)
                return self.transcription
