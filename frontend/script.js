const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("pdfFile");
const uploadText = document.getElementById("uploadText");
const loader = document.getElementById("loader");
const status = document.getElementById("status");
const previewFrame = document.getElementById("previewFrame");


uploadArea.addEventListener("click", () => {
    fileInput.click();
});


fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        uploadText.innerText = "📄 " + fileInput.files[0].name;
    }
});

async function processPDF(event) {
    
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
    previewFrame.classList.add("hidden"); 

    try {
        const response = await fetch("https://armaan2005-ai-pdf-studio.hf.space/process", {
            method: "POST",
            body: formData
        });

        
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json();
            loader.classList.add("hidden");
            
            
            status.innerText = "API Error: " + (errorData.error || "Quota limit exceeded or backend error.");
            status.style.color = "#ff4d4d"; // Red color
            return; 
        }

        if (!response.ok) {
            loader.classList.add("hidden");
            status.innerText = "Error: Server returned status " + response.status;
            status.style.color = "#ff4d4d";
            return;
        }

    
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

       
        previewFrame.src = url;
        previewFrame.classList.remove("hidden");

        
        const a = document.createElement("a");
        a.href = url;
        a.download = "edited.pdf";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        
        loader.classList.add("hidden");
        status.innerText = "✨ PDF Generated & Downloaded Successfully!";
        status.style.color = "#00c896";

        loader.classList.add("hidden");
        status.innerText = "✨ PDF Generated Successfully!";
        status.style.color = "#00c896"; 

    } catch (err) {
        loader.classList.add("hidden");
        console.error(err);
        status.innerText = "Something went wrong. Backend chalu hai na?";
        status.style.color = "#ff4d4d";
    }
}