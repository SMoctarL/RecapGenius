class TextProcessor:
    def __init__(self):
        pass

    def clean_subtitles(self, subtitles):
        """Nettoie et structure le texte des sous-titres."""
        cleaned_text = ""
        
        for subtitle in subtitles:
            text = subtitle['text']
            # Suppression des caractères spéciaux et timestamps
            text = text.replace('\n', ' ')
            text = ' '.join(text.split())
            cleaned_text += text + " "
        
        return cleaned_text.strip()

    def format_to_bullets(self, text):
        """Convertit le texte en format bullet points."""
        sentences = text.split('. ')
        return '\n'.join([f"• {sentence}" for sentence in sentences if sentence]) 