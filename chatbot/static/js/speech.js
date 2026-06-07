const micBtn = document.getElementById("micBtn");
const messageInput = document.getElementById("messageInput");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    micBtn.addEventListener("click", () => {

        micBtn.innerHTML = "🎙️";

        recognition.start();
    });

    recognition.onresult = (event) => {

        let transcript = "";

        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            transcript +=
                event.results[i][0].transcript;
        }

        messageInput.value = transcript;
    };

    recognition.onend = () => {

        micBtn.innerHTML = "🎤";

        console.log("Speech ended");
    };

    recognition.onerror = (event) => {

        micBtn.innerHTML = "🎤";

        console.log(event.error);
    };

} else {

    alert(
        "Speech Recognition not supported in this browser."
    );
}