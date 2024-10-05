from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# URL of the E-Ink Display Server (replace with the actual IP of your e-ink display server)
EINK_SERVER_URL = "http://localhost:8080"

@app.route("/")
def index():
    return render_template("index.html")

# Route to trigger weather update on the e-ink display server
@app.route("/trigger_weather", methods=["POST"])
def trigger_weather():
    try:
        response = requests.get(f"{EINK_SERVER_URL}/render_weather/")
        response.raise_for_status()  # Raises an exception if the status code is not 2xx
        return "Weather update triggered", 200
    except requests.exceptions.RequestException as e:
        print(f"Error triggering weather: {e}")
        return "Error", 500

@app.route("/trigger_image/", methods=["POST"])
def trigger_image():
    data = request.get_json()
    prompt = data.get('prompt', '')
    print(f"Prompt received: {prompt}")
    try:
        # Trigger the image generation
        response = requests.get(f"{EINK_SERVER_URL}/random_image/?prompt={prompt}")
        response.raise_for_status()  # Raises an exception if the status code is not 2xx
        return "Image generation triggered", 200
    except requests.exceptions.RequestException as e:
        print(f"Error triggering image: {e}")
        return "Error", 500
@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)