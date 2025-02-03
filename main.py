from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://weather.tsukumijima.net/api/forecast"


@app.route("/", methods=["GET", "POST"])
def index():
    city_code = "130010"  # デフォルト: 東京
    if request.method == "POST":
        city_code = request.form["city"]

    # APIリクエスト
    response = requests.get(f"{API_URL}?city={city_code}")
    data = response.json()

    # 天気データを取得
    forecasts = []
    for forecast in data["forecasts"][:3]:  # 今日・明日・明後日の天気
        forecasts.append({
            "date": forecast["dateLabel"],
            "telop": forecast["telop"],
            "image": forecast["image"]["url"],
            "temperature": {
                "max":
                forecast["temperature"]["max"]["celsius"]
                if forecast["temperature"]["max"] else "N/A",
                "min":
                forecast["temperature"]["min"]["celsius"]
                if forecast["temperature"]["min"] else "N/A",
            }
        })

    return render_template("index.html",
                           forecasts=forecasts,
                           selected_city=city_code)


if __name__ == "__main__":
    app.run(debug=True)

# test
