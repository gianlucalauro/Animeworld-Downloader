let animeLink = '';
let totalEpisodes = 0;

function setAnimeData(link, episodes) {
    animeLink = link;
    totalEpisodes = episodes;
}

function downloadEpisodes() {
    const episodeRange = document.getElementById('episodeRange').value.trim();
    let episodes = [];

    if (episodeRange.toLowerCase() === 'tutti' || episodeRange === '') {
        for (let i = 1; i <= totalEpisodes; i++) {
            episodes.push(i);
        }
    } else {
        episodes = episodeRange.split(',').map(ep => parseInt(ep.trim())).filter(ep => !isNaN(ep) && ep > 0 && ep <= totalEpisodes);
    }

    const requestData = {
        link: animeLink
    };

    if (episodes.length > 0) {
        requestData.episodes = episodes;
    }

    if (episodes.length > 0 || episodeRange === '') {
        fetch('/api/download?strm=true', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        }).then(response => response.json())
          .then(data => {
              alert('Download completato!');
              $('#downloadModal').modal('hide');
          })
          .catch(error => {
              console.error('Errore:', error);
              alert('Si è verificato un errore durante il download.');
          });
    } else {
        alert('Inserisci un range valido di episodi.');
    }
}
