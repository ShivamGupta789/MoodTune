const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const emotionText = document.getElementById("emotion");
const confidenceText = document.getElementById("confidence");

// Start camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        alert("Camera access denied");
    });

function captureImage() {
    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(sendToBackend, "image/jpeg");
}

function sendToBackend(blob) {
    const formData = new FormData();
    formData.append("file", blob, "capture.jpg");

    fetch("/detect-emotion", {
    method: "POST",
    body: formData
})

    .then(res => res.json())
    .then(data => {
    if (data.emotion) {
        emotionText.innerText = "Emotion: " + data.emotion;

        const confidence =
            typeof data.confidence === "number"
                ? (data.confidence * 100).toFixed(1) + "%"
                : "--";

        confidenceText.innerText = "Confidence: " + confidence;
    } else {
        emotionText.innerText = "Error detecting emotion";
        confidenceText.innerText = "";
    }
    const emotionColors = {
    Happy: "#4caf50",
    Sad: "#2196f3",
    Angry: "#f44336",
    Neutral: "#9e9e9e",
    Surprise: "#ff9800"
};

document.body.style.background =
    emotionColors[data.emotion] || "#1d2671";
document.getElementById("confidenceBar").style.width =
    (confidenceValue * 100) + "%";

});
}
