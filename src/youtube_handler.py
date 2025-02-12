from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import re

class YouTubeHandler:
    def __init__(self):
        self.transcript = None
        self.video_info = None
        self.video_title = "Vidéo YouTube"  # Titre par défaut

    def extract_video_id(self, url):
        """Extrait l'ID de la vidéo depuis l'URL YouTube."""
        video_id = None
        if "youtube.com/watch?v=" in url:
            video_id = url.split("watch?v=")[1][:11]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1][:11]
        return video_id

    def get_video_title(self, url):
        """Récupère le titre de la vidéo de manière sécurisée."""
        try:
            yt = YouTube(url)
            self.video_title = yt.title
        except:
            # En cas d'erreur, on utilise l'ID de la vidéo comme titre
            video_id = self.extract_video_id(url)
            self.video_title = f"Vidéo YouTube - {video_id}"
        return self.video_title

    def get_subtitles(self, url, language='fr'):
        """Récupère les sous-titres d'une vidéo YouTube."""
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                raise ValueError("URL YouTube invalide")

            # Récupération du titre
            self.get_video_title(url)
            
            try:
                # Récupération des sous-titres
                self.transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
                return self.transcript
            except:
                # Essai avec l'anglais si la langue demandée n'est pas disponible
                self.transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                return self.transcript

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des sous-titres: {str(e)}") 