from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
from youtube_handler import YouTubeHandler
from text_processor import TextProcessor
from summarizer import Summarizer
import os
import traceback

# Modifiez cette ligne pour pointer vers le bon dossier templates
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)
app.secret_key = os.urandom(24)

youtube_handler = YouTubeHandler()
text_processor = TextProcessor()
summarizer = Summarizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_video():
    try:
        print("Début de la requête de résumé")
        data = request.json
        print(f"Données reçues : {data}")

        if not data:
            print("Erreur: Aucune donnée reçue")
            return jsonify({
                'success': False,
                'error': 'Aucune donnée reçue'
            }), 400

        url = data.get('url')
        print(f"URL reçue : {url}")

        if not url:
            print("Erreur: URL manquante")
            return jsonify({
                'success': False,
                'error': 'URL manquante'
            }), 400

        length = data.get('length', 'medium')
        format_type = data.get('format', 'paragraph')
        language = data.get('language', 'fr')
        print(f"Paramètres : length={length}, format={format_type}, language={language}")

        # Récupération des sous-titres
        print("Tentative de récupération des sous-titres...")
        subtitles = youtube_handler.get_subtitles(url, language)
        print(f"Sous-titres récupérés : {bool(subtitles)}")

        if not subtitles:
            print("Erreur: Impossible de récupérer les sous-titres")
            return jsonify({
                'success': False,
                'error': 'Impossible de récupérer les sous-titres'
            }), 400
        
        # Nettoyage du texte
        print("Nettoyage du texte...")
        clean_text = text_processor.clean_subtitles(subtitles)
        print(f"Longueur du texte nettoyé : {len(clean_text) if clean_text else 0}")

        if not clean_text:
            print("Erreur: Texte vide après nettoyage")
            return jsonify({
                'success': False,
                'error': 'Texte vide après nettoyage'
            }), 400
        
        # Génération du résumé
        print("Génération du résumé...")
        summary = summarizer.summarize(clean_text, length, format_type)
        print("Résumé généré avec succès")
        
        return jsonify({
            'success': True,
            'summary': summary,
            'title': youtube_handler.video_title
        })

    except Exception as e:
        error_details = traceback.format_exc()
        print("=== ERREUR DÉTAILLÉE ===")
        print(error_details)
        print("=======================")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': error_details
        }), 400

if __name__ == '__main__':
    app.run(debug=True) 