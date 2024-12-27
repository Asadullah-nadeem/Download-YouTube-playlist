document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const form = document.getElementById("download-form");
    const logArea = document.getElementById("log");
    const stopButton = document.getElementById("stop-btn");

    let downloadId = Date.now();

    socket.on("log", (data) => {
        logArea.value += data.message + "\n";
        logArea.scrollTop = logArea.scrollHeight;
    });

    socket.on("download_complete", (data) => {
        if (data.id === downloadId) {
            stopButton.style.display = "none";
            alert("Download complete!");
        }
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const url = document.getElementById("url").value;
        const type = document.querySelector('input[name="type"]:checked').value;
        const resolution = document.getElementById("resolution").value;

        const requestBody = { id: downloadId, url, type };
        if (type === "video") {
            requestBody.resolution = resolution;
        }

        fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody),
        });

        stopButton.style.display = "block";
    });

    stopButton.addEventListener("click", () => {
        fetch("/stop", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: downloadId }),
        });
    });

    document.querySelectorAll('input[name="type"]').forEach((radio) => {
        radio.addEventListener("change", (event) => {
            const resolutionOptions = document.getElementById("resolution-options");
            resolutionOptions.style.display = event.target.value === "video" ? "block" : "none";
        });
    });
});
