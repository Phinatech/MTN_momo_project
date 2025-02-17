document.getElementById("upload-form").addEventListener("submit", function(event) {
    // Get the form inputs
    var fileInput = document.querySelector('input[name="file"]');
    var textInput = document.querySelector('textarea[name="text"]');
    var errorMessage = document.getElementById("validation-error");
    var submitBtn = document.getElementById("submit-btn");
    var loadingSpinner = document.getElementById("loading-spinner");

    // Check if both file and text inputs are empty
    if (!fileInput.files.length && !textInput.value.trim()) {
        event.preventDefault(); // Prevent form submission
        
        // Display validation error message
        errorMessage.style.display = "block";
        errorMessage.innerText = "Please upload a file or enter text before submitting.";
        
        // Scroll to the error message for visibility
        errorMessage.scrollIntoView({ behavior: "smooth" });

        return;
    }

    // Hide validation error if input is valid
    errorMessage.style.display = "none";

    // Disable the submit button to prevent multiple clicks
    submitBtn.disabled = true;

    // Show the loading spinner
    loadingSpinner.style.display = "block";

    // Initially disable the submit button
    submitBtn.disabled = true;

    // Add an event listener to check when a file is selected
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            submitBtn.disabled = false; // Enable button if a file is selected
        } else {
            submitBtn.disabled = true; // Keep disabled if no file is selected
        }
    });
});
