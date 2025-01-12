from speechtotext import SpeechToText
from SpeechSimplify import SimplifyText
from flask import Flask, render_template
import json
import time
import threading


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


def run_app():
    app.run(debug=False)


def main():
    flask_thread = threading.Thread(target=run_app)
    flask_thread.daemon = True
    flask_thread.start()

    data = {"text": {"original": None, "simplified": None}, "mic_on": True}
    with open("static/current_state.json", 'w') as f:
        json.dump(data, f)
    
    speech = SpeechToText(model_task='translate')
    while True:
        try:
            with open("static/current_state.json", 'r') as f:
                data = json.load(f)

            if data["mic_on"]:
                speech.transcribe()
                match len(speech.transcription):
                    case 1:
                        data["text"]["original"] = speech.transcription[0]
                    case 2:
                        data["text"]["original"] = speech.transcription[0]
                        data["text"]["simplified"] = speech.transcription[1]
                data["mic_on"] = False

                with open("static/current_state.json", 'w') as f:
                    json.dump(data, f)
            time.sleep(0.25)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
