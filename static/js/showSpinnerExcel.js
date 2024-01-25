document.addEventListener("DOMContentLoaded", function () {
    const exportButton = document.getElementById("export-excel-button");
    const spinnerContainer = document.getElementById("spinner-container");

    if (exportButton) {
        exportButton.addEventListener("click", function(e) {
            showSpinner(spinnerContainer);
            console.log("in exportBuut")
        });
    }
    
    // Detect when a file download starts
    document.onreadystatechange = function () {
        console.log("onreadystatechange")
        if (document.readyState === 'loading') {
            console.log("onreadystatechange loading")
            hideSpinner(spinnerContainer);
        }
    };

    function showSpinner(container) {
        container.removeAttribute("hidden");
      
        const spinner = document.createElement("div");
        const message = document.createElement("p");
      
        spinner.className = "spinner";
        message.className = "spinner-message";
        message.textContent = "Cargando...";
      
        container.innerHTML = ""; // Clear existing content
        container.appendChild(spinner);
        container.appendChild(message);
      }
      
      // Function to hide the spinner
      function hideSpinner(container) {
        container.setAttribute("hidden", true);
        container.innerHTML = ""; // Clear the spinner
      }
});
