document.addEventListener('DOMContentLoaded', function() {
    var yearSpan = document.getElementById('dynamic-year');
    if (yearSpan) {
      yearSpan.textContent = new Date().getFullYear();
    }
  });
  