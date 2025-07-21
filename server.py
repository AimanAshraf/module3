"""
This is the main server file for our Emotion Detection web app.

It uses Flask to handle the frontend and backend connection,
and calls our emotion detection logic to analyze user input.
"""
from flask import Flask, request, render_template, send_from_directory
from EmotionDetection.emotion_detection import emotion_detector
app = Flask(__name__)
@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Helps the app serve static files (like JS, CSS, images) when requested.
    """
    return send_from_directory('static', filename)
@app.route('/')
def index():
    """
    Displays the homepage when users visit the site.
    """
    return render_template('index.html')
@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    """
    Takes in a piece of text from the user and returns the emotions detected.

    If the user sends empty or invalid input, the function gives a helpful
    error message instead of crashing or returning nothing.
    """
    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    if not text_to_analyze:
        return "Invalid text! Please try again!", 400
    response = emotion_detector(text_to_analyze)
    if not response or response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!", 400
    result = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )
    return result, 200
if __name__ == '__main__':
    app.run(debug=True, port=5000)
