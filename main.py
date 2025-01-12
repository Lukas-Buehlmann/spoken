from speechtotext import SpeechToText
from SpeechSimplify import SimplifyText
from speechcleanup import CleanText


def main():
    speech = SimplifyText(model_task='transcribe')
    speech.transcribe()


if __name__ == "__main__":
    main()
