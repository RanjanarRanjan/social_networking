function selectTab(event, tabName) {
    event.preventDefault();

    var listItems = document.querySelectorAll(".jumpingButton ul li");

    listItems.forEach(function (item) {
        item.classList.remove("active");
    });

    var selectedItem = event.target.parentNode;
    selectedItem.classList.add("active");

    if (tabName === "followers") {
        // Call a function to render followers
        renderFollowers();
    } else {
        // Call a function to render feeds
        renderFeeds();
    }
}

function renderFollowers() {
    // Example: Render followers
    var followerListContainer = document.querySelector(".feedCard");
    if (followerListContainer) {
        // Clear previous content
        followerListContainer.innerHTML = "";

        // Example: Render each follower
        var followers = getFollowers(); // Assuming you have a function to get followers
        followers.forEach(function (follower) {
            var followerElement = document.createElement("div");
            followerElement.textContent = follower.name;
            followerListContainer.appendChild(followerElement);
        });
    }
}

function renderFeeds() {
    // Example: Render feeds
    var feedCardContainer = document.querySelector(".feedCard");
    if (feedCardContainer) {
        // Clear previous content
        feedCardContainer.innerHTML = "";

        // Example: Render each feed
        var feeds = getFeeds(); // Assuming you have a function to get feeds
        feeds.forEach(function (feed) {
            var feedElement = document.createElement("div");
            // Render feed content
            feedElement.textContent = feed.content;
            feedCardContainer.appendChild(feedElement);
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var firstTab = document.querySelector(".jumpingButton ul li:first-child");
    firstTab.classList.add("active");

    // Initially render feeds
    renderFeeds();
});
// Define the getFeeds function
function getFeeds() {
    // Your logic to fetch feeds goes here
}

// Other functions and code related to follower list
// Define the getFollowers function
function getFollowers() {
    // Your logic to fetch followers goes here
}
