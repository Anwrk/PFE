document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("testimonials-slider");

    slider.addEventListener("animationiteration", () => {
        slider.style.animation = "none"; // Reset animation
        void slider.offsetWidth; // Trigger reflow
        slider.style.animation = ""; // Restart animation
    });
});