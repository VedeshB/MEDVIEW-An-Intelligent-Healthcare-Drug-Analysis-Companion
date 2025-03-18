function showSuggestions(query) {
    if (query.length === 0) {
        document.getElementById("suggestions").innerHTML = "";
        return;
    }

    fetch(`/suggestions?query=${query}`)
        .then(response => response.json())
        .then(data => {
            let suggestionsHTML = data.map(item => `<div class="suggestion-item" onclick="selectSuggestion('${item}')">${item}</div>`).join('');
            document.getElementById("suggestions").innerHTML = suggestionsHTML;
        })
        .catch(error => console.error("Error fetching suggestions:", error));
}

function selectSuggestion(value) {
    document.getElementById("diseaseInput").value = value;
    document.getElementById("suggestions").innerHTML = "";
}
