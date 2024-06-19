function speak(myString) {
    // Display the text being spoken
    document.getElementById('spoken-text').textContent = myString;

    // Create a SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance(myString);
    const voices = speechSynthesis.getVoices();
    console.log(voices);
    utterance.voice = voices[14];
    utterance.rate = 0.2;
    speechSynthesis.speak(utterance);
}

// var apiUrl = "https://udl01sethtst02.vuhl.root.mrc.local/alerts?state=" // SERVER LINK

function callBackendAlerts() {
    var apiUrl = "https://0.0.0.0/alerts?state=" // DEV LINK
    let queryState = document.getElementById('query-state');
    let requestUrl = apiUrl + queryState.value;
    document.getElementById('spoken-text').textContent = "Fetching weather alerts...";
    console.log(requestUrl);

    fetch(requestUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(jsonBody => {
            console.log(jsonBody);
            let alertMessages = jsonBody[0];
            let readableMessage = '';

            for (let alert in alertMessages) {
                readableMessage += `${alert}: ${alertMessages[alert]}\n\n`;
            }

            speak(readableMessage);
        })
        .catch(error => {
            console.error('Error:', error);
            speak('There was an error fetching the weather alerts. Please try again later. There may be no alerts.');
        });
}

function callBackendForecast() {
    var apiUrl = "https://0.0.0.0/forecast?state=" // DEV LINK
    let queryState = document.getElementById('query-state');
    let queryCounty = document.getElementById('query-county').value;
    let requestUrl = apiUrl + queryState.value;
    requestUrl += "&county=";
    requestUrl += queryCounty;
    document.getElementById('spoken-text').textContent = "Fetching forecast...";
    console.log(requestUrl);

    fetch(requestUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(jsonBody => {
            console.log(jsonBody);
            let alertMessages = jsonBody[0];
            let readableMessage = '';

            for (let alert in alertMessages) {
                readableMessage += `${alert}: ${alertMessages[alert]}\n\n`;
            }

            speak(readableMessage);
        })
        .catch(error => {
            console.error('Error:', error);
            speak('There was an error fetching the weather alerts. Please try again later. There may be no alerts.');
        });
}