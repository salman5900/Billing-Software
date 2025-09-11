function openPopup() {
    const overlay = document.getElementById('popupOverlay');
    const content = document.getElementById('popupContent');

    overlay.classList.remove('hidden');

    setTimeout(() => {
        content.classList.remove('opacity-0', 'scale-90');
        content.classList.add('opacity-100', 'scale-100');
    }, 50);
}

function closePopup() {
    const overlay = document.getElementById('popupOverlay');
    const content = document.getElementById('popupContent');

    content.classList.remove('opacity-100', 'scale-100');
    content.classList.add('opacity-0', 'scale-90');

    setTimeout(() => {
        overlay.classList.add('hidden');
    }, 400);
}

// Handle button click
document.getElementById("exploreBtn").addEventListener("click", (e) => {
    e.stopPropagation(); // prevent immediate close
    openPopup();
});

// Close when clicking outside
document.getElementById("popupOverlay").addEventListener("click", (e) => {
    const content = document.getElementById("popupContent");
    if (!content.contains(e.target)) {
        closePopup();
    }
});
