const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("pdfFile");
const uploadText = document.getElementById("uploadText");
const loader = document.getElementById("loader");
const status = document.getElementById("status");
const previewFrame = document.getElementById("previewFrame");

// File picker open
uploadArea.addEventListener("click", () => {
    fileInput.click();
});

// File selected
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        uploadText.innerText = "📄 " + fileInput.files[0].name;
    }
});

async function processPDF(event) {
    // 1. Page refresh hone se rokne ke liye
    if (event) event.preventDefault(); 

    if (!fileInput.files[0]) {
        alert("Upload a PDF first");
        return;
    }

    const prompt = document.getElementById("prompt").value;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("prompt", prompt);

    // UI Reset for new request
    loader.classList.remove("hidden");
    status.innerText = "Processing... Please wait.";
    status.style.color = "white"; 
    previewFrame.classList.add("hidden"); // Puraana preview hide kar do

    try {
        const response = await fetch("http://127.0.0.1:8000/process", {
            method: "POST",
            body: formData
        });

        // 🛑 SMART CHECK: Kya response JSON (Error) hai?
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json();
            loader.classList.add("hidden");
            
            // Error ko status mein show karo (laal rang mein)
            status.innerText = "API Error: " + (errorData.error || "Quota limit exceeded or backend error.");
            status.style.color = "#ff4d4d"; // Red color
            return; // Yahan se aage mat badho
        }

        if (!response.ok) {
            loader.classList.add("hidden");
            status.innerText = "Error: Server returned status " + response.status;
            status.style.color = "#ff4d4d";
            return;
        }

     // ✅ Agar sab theek hai, toh PDF load karo
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // 1. SHOW PREVIEW
        previewFrame.src = url;
        previewFrame.classList.remove("hidden");

        // 2. 🛑 AUTO DOWNLOAD (Yeh wapas add kar diya)
        const a = document.createElement("a");
        a.href = url;
        a.download = "edited.pdf";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // 3. SUCCESS MESSAGE
        loader.classList.add("hidden");
        status.innerText = "✨ PDF Generated & Downloaded Successfully!";
        status.style.color = "#00c896";

        loader.classList.add("hidden");
        status.innerText = "✨ PDF Generated Successfully!";
        status.style.color = "#00c896"; // Green color

    } catch (err) {
        loader.classList.add("hidden");
        console.error(err);
        status.innerText = "Something went wrong. Backend chalu hai na?";
        status.style.color = "#ff4d4d";
    }
}