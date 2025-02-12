document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.input-container');
    const urlInput = document.getElementById('youtube-url');
    const lengthSelect = document.getElementById('length');
    const formatSelect = document.getElementById('format');
    const languageSelect = document.getElementById('language');
    const summarizeBtn = document.getElementById('summarize-btn');
    const resultContainer = document.querySelector('.result-container');
    const videoTitle = document.getElementById('video-title');
    const summaryContent = document.getElementById('summary-content');
    const loader = document.querySelector('.loader');

    summarizeBtn.addEventListener('click', async function() {
        const url = urlInput.value.trim();
        if (!url) {
            alert('Veuillez entrer une URL YouTube valide');
            return;
        }

        // Afficher le loader
        loader.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        summarizeBtn.disabled = true;

        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    length: lengthSelect.value,
                    format: formatSelect.value,
                    language: languageSelect.value
                })
            });

            const data = await response.json();

            if (data.success) {
                videoTitle.textContent = data.title;
                summaryContent.innerHTML = formatSummary(data.summary, formatSelect.value);
                resultContainer.classList.remove('hidden');
            } else {
                alert('Erreur: ' + data.error);
            }
        } catch (error) {
            alert('Une erreur est survenue: ' + error.message);
        } finally {
            loader.classList.add('hidden');
            summarizeBtn.disabled = false;
        }
    });

    function formatSummary(summary, format) {
        if (format === 'bullets') {
            return summary.split('\n').map(line => `<p>${line}</p>`).join('');
        } else if (format === 'mindmap') {
            return summary.split('\n').map(line => {
                const indent = line.match(/^\s*/)[0].length;
                return `<p style="margin-left: ${indent * 20}px">${line.trim()}</p>`;
            }).join('');
        }
        return `<p>${summary}</p>`;
    }
});