from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            truncation=True
        )
        self.max_chunk_length = 1024  # BART peut gérer jusqu'à 1024 tokens

    def chunk_text(self, text):
        """Découpe le texte en morceaux plus petits."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_length += len(word) + 1
            if current_length > self.max_chunk_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def summarize(self, text, max_length='medium', format='paragraph'):
        """
        Résume le texte en utilisant BART.
        max_length: 'short', 'medium', 'long'
        format: 'paragraph', 'bullets', 'mindmap'
        """
        # Définir la longueur maximale
        max_length_words = {
            'short': 60,
            'medium': 120,
            'long': 180
        }

        min_length_words = {
            'short': 30,
            'medium': 60,
            'long': 90
        }

        # Découper le texte en chunks
        chunks = self.chunk_text(text)
        
        # Résumer chaque chunk
        summaries = []
        for chunk in chunks:
            if len(chunk.split()) > 50:  # Ne résumer que les chunks assez longs
                summary = self.summarizer(
                    chunk,
                    max_length=max_length_words[max_length] // len(chunks),
                    min_length=min_length_words[max_length] // len(chunks),
                    do_sample=False,  # Plus déterministe
                    num_beams=4  # Meilleure qualité
                )[0]['summary_text']
                summaries.append(summary)
            elif chunk.strip():
                summaries.append(chunk)

        # Combiner les résumés
        combined_summary = ' '.join(summaries)

        # Faire un résumé final si nécessaire
        if len(combined_summary.split()) > max_length_words[max_length]:
            combined_summary = self.summarizer(
                combined_summary,
                max_length=max_length_words[max_length],
                min_length=min_length_words[max_length],
                do_sample=False,
                num_beams=4
            )[0]['summary_text']

        # Formater le résumé selon le format demandé
        if format == 'bullets':
            sentences = combined_summary.split('. ')
            combined_summary = '\n'.join([f"• {s.strip()}" for s in sentences if s.strip()])
        elif format == 'mindmap':
            sentences = combined_summary.split('. ')
            combined_summary = '• ' + sentences[0] + '\n' + '\n'.join([f"  - {s.strip()}" for s in sentences[1:] if s.strip()])

        return combined_summary