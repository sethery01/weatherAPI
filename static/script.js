function speak(myString) {
    // Display the text being spoken
    document.getElementById('spoken-text').textContent = myString;

    // Create a SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance(myString);

    // Load voices and select a specific one
    speechSynthesis.onvoiceschanged = function () {
        const voices = speechSynthesis.getVoices();
        console.log(voices);
        if (voices.length > 14) {
            utterance.voice = voices[14]; // Choose a specific voice, ensure index 14 exists
        }
        speechSynthesis.speak(utterance);
    };

    // Speak the text (if voices are already loaded)
    if (speechSynthesis.getVoices().length > 0) {
        const voices = speechSynthesis.getVoices();
        console.log(voices);
        if (voices.length > 14) {
            utterance.voice = voices[14]; // Choose a specific voice, ensure index 14 exists
        }
        speechSynthesis.speak(utterance);
    }
}

// Define the API URL
// var apiUrl = "https://udl01sethtst02.vuhl.root.mrc.local/alerts?state=";
var apiUrl = "https://0.0.0.0/alerts?state=" // DEV LINK

function callBackend() {
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
            speak('There was an error fetching the weather alerts. Please try again later.');
        });
}