
import time

from queue import Queue
from openai import OpenAI
import speech_recognition as sr


class SpeechToText:
    """
    A class for handling real-time speech-to-text and translation using
    Whisper-1 from OpenAI.
    """

    # time in seconds before recording callback is run again
    record_time_limit = 1

    # time in seconds between recording before a newline is added
    time_to_talk = 2

    def __init__(self, model_task='transcribe'):
        """

        :param model_task: set to 'translate' to turn on translation mode
        """
        self.data = Queue()
        self.model_task = model_task

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
        # self.source = sr.Microphone(sample_rate=16000)

        # requires that OPENAI_API_KEY is defined as environmental variable with openai license
        self.model = OpenAI()
        self.transcription = ['']

    def r_callback(self, _, audio_data):
        """
        Function to be called by 'speechrecognizer' that will add wav data to the queue
        in a separate thread
        :param _:
        :param audio_data: stores a speech_recognition.AudioData instance
        :return: None
        """
        wav_data = audio_data.get_wav_data()
        self.data.put(wav_data)

    def transcribe(self):
        """
        method to transcribe or translate audio in real-time storing all information into 'self.transcription'
        :return: None
        """
        # self.r.listen_in_background(self.source, self.r_callback)
        # time_talking = time.time()
        # done_talking = False
        # printed_index = 0
        self.transcription = []
        with sr.Microphone(sample_rate=16000) as source:
            print("listening...")
            self.r.pause_threshold = 4
            try:
                audio_data = self.r.listen(source, stream=False, phrase_time_limit=30, timeout=5)
            except sr.WaitTimeoutError:
                print("No audio given in time. No transcription possible")
                return
        data = audio_data.get_wav_data()

        with open("audio_data.wav", 'wb') as f:
            f.write(data)

        with open("audio_data.wav", 'rb') as f:
            if self.model_task == 'translate':
                result = self.model.audio.translations.create(file=f, model="whisper-1")
            else:
                result = self.model.audio.transcriptions.create(file=f, model="whisper-1")

        # store transcription and clean it up
        text = result.text.strip()
        self.transcription.append(text)
        print(text)

        # clear the file contents and make the file if it doesn't exist
        # open("audio_data.wav", 'wb').close()

        # print("beginning transcription")
        # while True:
        #     try:
        #         now = time.time()
        #         if not self.data.empty():
        #
        #             # set done talking to true if more than time to talk seconds passed
        #             done_talking = (now - time_talking > SpeechToText.time_to_talk)
        #             time_talking = now
        #
        #             # # concat all binary data in the queue and empty the queue
        #             # audio_data = b''.join(self.data.queue)
        #             # self.data.queue.clear()
        #             #
        #             # with open("temp_audio.wav", 'wb') as f:
        #             #     f.write(audio_data)
        #             #
        #             # wav_1 = AudioSegment.from_wav("temp_audio.wav")
        #             # try:
        #             #     wav_2 = AudioSegment.from_wav("audio_data.wav")
        #             #     combined_wav = wav_1 + wav_2
        #             #     combined_wav.export("audio_data.wav", format="wav")
        #             # except Exception:
        #             #     print("audio loading failed")
        #             #     wav_1.export("audio_data.wav", format="wav")
        #             #
        #             with open("audio_data.wav", 'wb') as f:
        #                 f.write(data)
        #
        #             with open("audio_data.wav", 'rb') as f:
        #                 if self.model_task == 'translate':
        #                     result = self.model.audio.translations.create(file=f, model="whisper-1")
        #                 else:
        #                     result = self.model.audio.transcriptions.create(file=f, model="whisper-1")
        #
        #             # store transcription and clean it up
        #             text = result.text.strip()
        #
        #             if done_talking:
        #                 self.transcription.append(text)
        #
        #                 # empties the wav file contents
        #                 # open("audio_data.wav", 'wb').close()
        #                 print(text)
        #             else:
        #                 self.transcription[-1] = text
        #                 # print(text)
        #
        #             # for i in range(len(self.transcription)):
        #             #     if i >= printed_index:
        #             #         print(self.transcription[i])
        #             #         printed_index += 1
        #         else:
        #             time.sleep(0.1)
        #     except KeyboardInterrupt:
        #         break
