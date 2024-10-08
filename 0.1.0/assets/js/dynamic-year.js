document.addEventListener('DOMContentLoaded', function () {
    const yearSpan = document.getElementById('dynamic-year');
    if (yearSpan) {
        const currentYear = new Date().getFullYear();
        yearSpan.textContent = currentYear;
    }
});
