const submitBtn = document.getElementById("submitBtn");
const statusDiv = document.getElementById("status");

submitBtn.addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    const promptInput = document.getElementById("promptInput");

    if (!fileInput.files.length) {
        alert("Please upload a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("prompt", promptInput.value);

    statusDiv.innerText = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/process", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "edited.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();

        statusDiv.innerText = "Download started!";

    } catch (error) {
        statusDiv.innerText = "Error processing PDF.";
    }
});