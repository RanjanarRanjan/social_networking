function openNotifications() {
    var modal = document.getElementById("notificationModal");
    modal.style.display = "block";

    // Fetch and display notifications (example)
    fetchNotifications();
}

function closeNotifications() {
    var modal = document.getElementById("notificationModal");
    modal.style.display = "none";
}

function fetchNotifications() {
    // Example: Fetch notifications from server
    // Replace this with your actual logic to fetch notifications
    var notifications = [
        "Notification 1",
        "Notification 2",
        "Notification 3"
    ];

    var notificationList = document.getElementById("notificationList");
    notificationList.innerHTML = ""; // Clear previous notifications

    // Append fetched notifications to the list
    notifications.forEach(function(notification) {
        var li = document.createElement("li");
        li.textContent = notification;
        notificationList.appendChild(li);
    });
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById("notificationModal");
    if (event.target == modal) {
        closeNotifications();
    }
}
