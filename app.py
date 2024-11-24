from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# URL of the E-Ink Display Server (replace with the actual IP of your e-ink display server)
EINK_SERVER_URL = "http://192.168.100.31:8080"
RPI3_SERVER_URL = "http://192.168.100.179:5005"

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

@app.route("/trigger_last", methods=["POST"])
def trigger_last():
    try:
        response = requests.get(f"{RPI3_SERVER_URL}/last")
        response.raise_for_status()  # Raises an exception if the status code is not 2xx
        return "Weather update triggered", 200
    except requests.exceptions.RequestException as e:
        print(f"Error triggering weather: {e}")
        return "Error", 500
@app.route("/trigger_random", methods=["POST"])
def trigger_random():
    try:
        response = requests.get(f"{RPI3_SERVER_URL}/random")
        response.raise_for_status()  # Raises an exception if the status code is not 2xx
        return "Weather update triggered", 200
    except requests.exceptions.RequestException as e:
        print(f"Error triggering weather: {e}")
        return "Error", 500

@app.route("/view", methods=["POST"])
def view():
    data = request.get_json()
    filepath = data.get('filepath', '')
    print(f"Filepath received: {filepath}")
    try:
        response = requests.get(f"{RPI3_SERVER_URL}/view/{filepath}")
        response.raise_for_status()  # Raises an exception if the status code is not 2xx
        return "Weather update triggered", 200
    except requests.exceptions.RequestException as e:
        print(f"Error triggering weather: {e}")
        return "Error", 500

@app.route("/images", methods=["GET"])
def get_images():
    try:
        response = requests.get(f"{RPI3_SERVER_URL}/images")
        response.raise_for_status()  # Raises an exception if the status code is not 2xx
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        print(f"Error fetching images: {e}")
        return "Error", 500

@app.route("/trigger_image", methods=["POST"])
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
    error_message = request.args.get('message', 'Unknown error')
    return render_template("error.html",error_message=error_message)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
