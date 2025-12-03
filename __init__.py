from flask import Flask, render_template, jsonify
from datetime import datetime
import Request  # ← IMPORTANT : utiliser requests, pas urllib

app = Flask(__name__)

# VOS ROUTES EXISTANTES
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/tawarano/')
def tawarano():
    return render_template("tawarano.html")

@app.route('/rapport/')
def mongraphique():
    return render_template("graphique.html")

@app.route('/histogramme/')
def histogramme():
    return render_template("histogramme.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

# ROUTES POUR L'EXERCICE 6
@app.route('/commits/')
def commits():
    return render_template("commits.html")

@app.route('/commits-data/')
def commits_data():
    # ⚠️ REMPLACEZ "camslt" PAR VOTRE VRAI USERNAME GITHUB ⚠️
    username = "camcamslt"  # ← CHANGEZ ICI
    repo = "5MCSI_Métriques_camille"
    
    api_url = f"https://api.github.com/repos/{username}/{repo}/commits"
    
    try:
        # Utiliser requests (pas urllib !)
        response = requests.get(api_url, timeout=10)
        
        # Vérifier les erreurs
        if response.status_code == 404:
            return jsonify({
                'error': 'Repository non trouve',
                'message': f'Le repo {username}/{repo} n\'existe pas ou est prive',
                'resultats': []
            }), 404
        
        if response.status_code != 200:
            return jsonify({
                'error': f'Erreur GitHub: {response.status_code}',
                'resultats': []
            }), 500
        
        commits_list = response.json()
        
        # Compter les commits par minute
        minutes_count = {i: 0 for i in range(60)}
        
        for commit in commits_list:
            try:
                date_str = commit['commit']['author']['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minute = date_obj.minute
                minutes_count[minute] += 1
            except (KeyError, ValueError):
                continue
        
        # Préparer les résultats
        resultats = []
        for minute in range(60):
            resultats.append({
                'minute': minute,
                'count': minutes_count[minute]
            })
        
        return jsonify({'resultats': resultats})
    
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Timeout',
            'message': 'GitHub met trop de temps a repondre',
            'resultats': []
        }), 500
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Erreur de connexion',
            'message': str(e),
            'resultats': []
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Erreur interne',
            'message': str(e),
            'resultats': []
        }), 500

if __name__ == '__main__':
    app.run()
