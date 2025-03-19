document.addEventListener("DOMContentLoaded", () => {
    const cookieAlert = document.getElementById("cookie-alert");
    const acceptButton = document.getElementById("accept-cookies");

    // Check if cookies were already accepted
    if (localStorage.getItem("cookiesAccepted") === "true") {
        cookieAlert.style.display = "none";
    }

    // Handle cookie acceptance
    acceptButton.addEventListener("click", () => {
        localStorage.setItem("cookiesAccepted", "true");
        cookieAlert.style.display = "none";
    });
});

