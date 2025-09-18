from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>🌦 Weather App</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to top, #89f7fe, #66a6ff);
            overflow: hidden;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Cloud animation */
        .cloud {
            position: absolute;
            background: white;
            border-radius: 50%;
            opacity: 0.8;
            animation: floatClouds 60s linear infinite;
        }
        .cloud::before, .cloud::after {
            content: '';
            position: absolute;
            background: white;
            border-radius: 50%;
        }
        .cloud.small {
            width: 80px; height: 50px; top: 20%;
            left: -100px;
            animation-duration: 80s;
        }
        .cloud.large {
            width: 200px; height: 100px; top: 40%;
            left: -200px;
            animation-duration: 100s;
        }
        .cloud::before {
            width: 60%; height: 60%;
            top: -30%; left: 10%;
        }
        .cloud::after {
            width: 70%; height: 70%;
            top: -20%; right: 10%;
        }
        @keyframes floatClouds {
            from { transform: translateX(0); }
            to { transform: translateX(120vw); }
        }

        /* Weather box */
        .container {
            position: relative;
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            width: 400px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            animation: fadeIn 1.2s ease-in-out;
            z-index: 10;
        }
        h1 {
            margin-bottom: 10px;
            color: #2c3e50;
        }
        input[type="text"] {
            padding: 10px;
            width: 75%;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
        }
        button {
            padding: 10px 20px;
            border: none;
            background: #3498db;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background: #2980b9;
            transform: scale(1.05);
        }
        .weather {
            margin-top: 15px;
            animation: slideUp 1s ease-in-out;
        }
        .forecast {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .day {
            background: #ecf0f1;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9);}
            to { opacity: 1; transform: scale(1);}
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px);}
            to { opacity: 1; transform: translateY(0);}
        }
    </style>
</head>
<body>
    <!-- Clouds -->
    <div class="cloud small"></div>
    <div class="cloud large"></div>

    <div class="container">
        <h1>☁ Weather App</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter city name" required>
            <br>
            <button type="submit">Get Weather</button>
        </form>

        {% if weather %}
        <div class="weather">
            <h2>{{ city }}</h2>
            <p>🌡 Temp: {{ weather['current_condition'][0]['temp_C'] }} °C</p>
            <p>💧 Humidity: {{ weather['current_condition'][0]['humidity'] }} %</p>
            <p>🌥 Condition: {{ weather['current_condition'][0]['weatherDesc'][0]['value'] }}</p>
        </div>

        <h3>📅 7-Day Forecast</h3>
        <div class="forecast">
            {% for day in weather['weather'] %}
            <div class="day">
                <strong>{{ day['date'] }}</strong><br>
                🌡 Max: {{ day['maxtempC'] }}°C<br>
                🌡 Min: {{ day['mintempC'] }}°C<br>
                🌥 {{ day['hourly'][4]['weatherDesc'][0]['value'] }}
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    city = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
    return render_template_string(html_template, weather=weather, city=city)

if __name__ == "__main__":
    app.run(debug=False)
