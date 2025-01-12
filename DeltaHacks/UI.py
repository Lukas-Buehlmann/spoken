from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
