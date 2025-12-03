from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen, Request
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact/')
def contact():
    return render_template("contact.html")
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/histogramme/')
def histogramme():
    return render_template("histogramme.html")
  
GITHUB_COMMITS_URL = "https://api.github.com/repos/camcalslt/5MCSI_Metriques_camille/commits"
  

@app.route("/commits-data/")
def commits_data():
    """
    Retourne le nombre de commits groupés par minute (0 à 59)
    au format JSON pour le graphique.
    """

    # GitHub aime bien avoir un User-Agent
    req = Request(GITHUB_COMMITS_URL, headers={"User-Agent": "Flask-App"})
    response = urlopen(req)
    raw_content = response.read()
    commits_list = json.loads(raw_content.decode("utf-8"))

    # Compteur de commits par minute (0–59)
    minutes_count = {m: 0 for m in range(60)}

    for commit in commits_list:
        # Les données qui nous intéressent : commit -> author -> date
        date_str = (
            commit.get("commit", {})
                  .get("author", {})
                  .get("date")
        )
        if not date_str:
            continue

        # Exemple de format : "2024-02-11T11:57:27Z"
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        minute = dt.minute
        minutes_count[minute] += 1

    # On renvoie une liste de dicts {minute, count}
    results = [
        {"minute": m, "count": minutes_count[m]}
        for m in range(60)
    ]

    return jsonify(results=results)


@app.route("/commits/")
def commits_page():
    # Page HTML avec le graphique
    return render_template("commits.html")

  
if __name__ == "__main__":
  app.run(debug=True)
