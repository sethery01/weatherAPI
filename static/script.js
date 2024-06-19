function speak(myString) {
    // Display the text being spoken
    document.getElementById('spoken-text').textContent = myString;

    // Create a SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance(myString);
    const voices = speechSynthesis.getVoices();
    console.log(voices);
    utterance.voice = voices[14];
    speechSynthesis.speak(utterance);
}

// Define the API URL
// var apiUrl = "https://udl01sethtst02.vuhl.root.mrc.local/alerts?state=";
// var apiUrl = "https://0.0.0.0/alerts?state=" // DEV LINK

function callBackend() {
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