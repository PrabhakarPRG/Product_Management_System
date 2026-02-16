// Smooth fade-in animation
document.addEventListener("DOMContentLoaded", () => {
  document.body.style.opacity = 0;
  setTimeout(() => {
    document.body.style.transition = "opacity 0.6s ease";
    document.body.style.opacity = 1;
  }, 100);
});

// Add ripple effect to buttons
document.querySelectorAll("button").forEach(btn => {
  btn.addEventListener("click", function(e) {
    const circle = document.createElement("span");
    circle.classList.add("ripple");
    this.appendChild(circle);

    const rect = this.getBoundingClientRect();
    circle.style.left = `${e.clientX - rect.left}px`;
    circle.style.top = `${e.clientY - rect.top}px`;

    setTimeout(() => circle.remove(), 600);
  });
});
