from speechtotext import SpeechToText
from SpeechSimplify import SimplifyText
from flask import Flask, render_template, request, jsonify
import webbrowser
import json
import time
from threading import Timer
from learning_sentiment import get_emotion

app = Flask(__name__)
speech = SpeechToText()
simple = SimplifyText()


@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text', '')  # Get the text input from the frontend
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Call the function from learning_sentiment.py
        results = get_emotion(text)
        response = [{'sentence': text, 'sentiment': sentiment, 'emoji': emoji} for sentiment, emoji in results]
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/start-mic', methods=['POST'])
def start_mic():
    """
    Flask endpoint to start the mic and return text output as JSON.
    """
    try:
        # Extract task and mode from the request body
        request_data = request.json
        task = request_data.get('task', 'transcribe')  # Default to 'transcribe'
        mode = request_data.get('mode', 'normal')  # Default to 'normal'

        result = None
        if mode == 'simple':
            simple.transcribe()
            result = {"text": {"original": simple.transcription[0], "simplified": simple.transcription[1]}}
            print("simple")
            print(simple.transcription[1])
        else:
            speech.model_task = task
            speech.transcribe()
            result = {"text": {"original": speech.transcription[0], "simplified": speech.transcription[1]}}

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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


def launch_web():
    webbrowser.open_new('http://127.0.0.1:5000/')


def run_app():
    Timer(1, launch_web).start()
    app.run(debug=False)


def main():
    run_app()
    # flask_thread = threading.Thread(target=run_app)
    # flask_thread.daemon = True
    # flask_thread.start()

    # data = {"text": {"original": None, "simplified": None}, "mic_on": True}
    # with open("static/current_state.json", 'w') as f:
    #     json.dump(data, f)
    #
    # while True:
    #     try:
    #         time.sleep(0.1)
    #     except KeyboardInterrupt:
    #         break

    # speech = SpeechToText(model_task='translate')
    # while True:
    #     try:
    #         with open("static/current_state.json", 'r') as f:
    #             data = json.load(f)
    #
    #         if data["mic_on"]:
    #             speech.transcribe()
    #             match len(speech.transcription):
    #                 case 1:
    #                     data["text"]["original"] = speech.transcription[0]
    #                 case 2:
    #                     data["text"]["original"] = speech.transcription[0]
    #                     data["text"]["simplified"] = speech.transcription[1]
    #             data["mic_on"] = False
    #
    #             with open("static/current_state.json", 'w') as f:
    #                 json.dump(data, f)
    #         time.sleep(0.25)
    #     except KeyboardInterrupt:
    #         break


if __name__ == "__main__":
    main()
