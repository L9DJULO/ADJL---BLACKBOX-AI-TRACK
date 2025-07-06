const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

if (!SpeechRecognition) {
  alert("L'API Web Speech n'est pas supportée par ce navigateur.");
} else {
  const recognition = new SpeechRecognition();
  recognition.lang = 'fr-FR';
  recognition.interimResults = true;
  recognition.continuous = false;

  const button = document.getElementById("start")!;
  const output = document.getElementById("transcript")!;

  button.addEventListener("click", () => {
    recognition.start();
    output.textContent = "🎙️ Écoute en cours...";
  });

  recognition.onresult = (event: SpeechRecognitionEvent) => {
    const transcript = Array.from(event.results)
      .map(result => result[0].transcript)
      .join('');
    output.textContent = transcript;
  };

  recognition.onerror = (event: any) => {
    output.textContent = `❌ Erreur : ${event.error}`;
  };

  recognition.onend = () => {
    console.log("Reconnaissance terminée.");
  };
}
