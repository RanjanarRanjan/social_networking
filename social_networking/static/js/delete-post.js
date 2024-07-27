function toggleDropdown(event) {
    event.stopPropagation(); // Prevent the click event from bubbling up
    var dropdown = event.target.nextElementSibling;
    dropdown.style.display =
        dropdown.style.display === "block" ? "none" : "block";
}

function deletePost() {
    // Replace this with your actual code to delete the post
    console.log("Post deleted");
}
