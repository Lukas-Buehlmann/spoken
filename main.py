from speechtotext import SpeechToText
from SpeechSimplify import SimplifyText
from speechcleanup import CleanText
from flask import Flask, render_template
import json
import time


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/transcription')
def transcription():
    return render_template('transcription.html')


@app.route('/translation')
def translation():
    return render_template('translation.html')


@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')


@app.route('/simplification')
def simplification():
    return render_template('simplification.html')


def main():
    app.run(debug=False)
    # speech = SimplifyText(model_task='transcribe')
    # while True:
    #     try:
    #         with open("current_state.json", 'r') as f:
    #             data = json.load(f)
    #
    #         if data["mic_on"]:
    #             speech.transcribe()
    #             match len(speech.transcription):
    #                 case 1:
    #                     data.text.original = speech.transcription[0]
    #                 case 2:
    #                     data.text.original = speech.transcription[0]
    #                     data.text.simplified = speech.transcription[1]
    #             data["mic_on"] = False
    #
    #             with open("current_state.json", 'w') as f:
    #                 json.dump(data, f)
    #         time.sleep(0.25)
    #     except KeyboardInterrupt:
    #         break


if __name__ == "__main__":
    main()
