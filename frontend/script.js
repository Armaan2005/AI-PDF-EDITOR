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
        const response = await fetch("http://localhost:8000/process", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.status === "success") {
            statusDiv.innerText = "PDF processed successfully!";
        } else {
            statusDiv.innerText = "Error occurred.";
        }

    } catch (error) {
        statusDiv.innerText = "Server error.";
    }
});