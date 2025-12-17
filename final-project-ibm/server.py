"""Flask web server for emotion detection application."""
from flask import Flask, request, render_template, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    """
    Analyze emotion from text provided as query parameter.
    
    Returns:
        Formatted emotion analysis or error message with HTTP 400 status.
    
    Example:
        GET /emotionDetector?textToAnalyze=I+am+happy
        Returns: "For the given statement, the system response is..."
    """
    # Get text from query parameter
    text_to_analyze = request.args.get('textToAnalyze')
    
    # Check for empty or blank input
    if not text_to_analyze or text_to_analyze.strip() == '':
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    
    # Call emotion detection function
    result = emotion_detector(text_to_analyze)
    
    # Check if API returned error (dominant_emotion is None)
    if result['dominant_emotion'] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    
    # Format successful response
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    
    return formatted_response

@app.route('/')
def index():
    """
    Render the main HTML page for the emotion detection application.
    
    Returns:
        Rendered index.html template.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)