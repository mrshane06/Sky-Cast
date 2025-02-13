from flask import Flask, render_template, request
from main import main as get_weather

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def index():
    current_weather = None
    forecast = None
    if request.method == 'POST':
        city = request.form['cityName']
        current_weather, forecast = get_weather(city)

    return render_template('search.html', data=current_weather, forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)