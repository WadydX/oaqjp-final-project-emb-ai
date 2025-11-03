"""
Flask web server for the Emotion Detection web application.
This module defines routes that receive user input, call the emotion detection
function from the EmotionDetection package, and return formatted results.
"""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """
    Handle emotion detection requests.
    Accepts user text input via GET or POST, validates it, calls the
    emotion_detector() function, and returns a formatted response.
    Returns an error message for blank or invalid inputs.
    """
    text_to_analyze = request.args.get("textToAnalyze") or request.form.get("textToAnalyze")

    # Validate input
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    response = emotion_detector(text_to_analyze)

    # Handle API 400 or invalid input
    if response.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    # Extract emotion scores
    anger = response["anger"]
    disgust = response["disgust"]
    fear = response["fear"]
    joy = response["joy"]
    sadness = response["sadness"]
    dominant = response["dominant_emotion"]

    # Build response text
    return (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )

@app.route("/")
def index():
    """
    Render the homepage for the web application.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
