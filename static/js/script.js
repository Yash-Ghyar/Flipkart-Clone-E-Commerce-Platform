console.log("E-Commerce UI Loaded");

/* Toggle search on mobile */
function toggleSearch() {
    let box = document.getElementById("mobileSearch");
    if (box.style.display === "none" || box.style.display === "") {
        box.style.display = "block";
    } else {
        box.style.display = "none";
    }
}
