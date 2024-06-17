function speak(myString) {
    // Create a SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance(myString);

    // Select a voice
    const voices = speechSynthesis.getVoices();
    console.log(voices)
    utterance.voice = voices[18]; // Choose a specific voice

    // Speak the text
    speechSynthesis.speak(utterance);
}

// Define the API URL
let apiUrl = "https://udl01sethtst02.vuhl.root.mrc.local/alerts?state=";
let form = document.getElementById('search-form')
// console.log(form)

form.onsubmit = function () {
    let queryState = document.getElementById('query-state')
    let requestUrl = apiUrl + queryState.value
    console.log(requestUrl);
   
    // Make a GET request
    fetch(requestUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log(response.json()) 
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
};