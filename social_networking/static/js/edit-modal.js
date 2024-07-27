document.addEventListener("DOMContentLoaded", function () {
    // Get the modal element
    var modal = document.getElementById("openEditModal");

    // Check if modal exists before assigning functions
    if (modal) {
        // Function to open the edit profile modal
        window.openEditModal = function () {
            modal.style.display = "block";
        }

        // Function to close the edit profile modal
        window.closeEditModal = function () {
            modal.style.display = "none";
        }

        // Close the modal when clicking outside of it
        window.onclick = function (event) {
            if (event.target === modal) {
                closeEditModal();
            }
        };

        // Attach click event listener to the edit button if exists
        var editButton = document.getElementById("editButton");
        if (editButton) {
            editButton.addEventListener("click", openEditModal);
        }
    }
});
