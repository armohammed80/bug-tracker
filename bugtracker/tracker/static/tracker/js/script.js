document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  if (form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
      form.addEventListener('submit', () => {
        submitButton.disabled = true;
        submitButton.innerText = 'Submitting...';
      });
    }
  }

  document.querySelectorAll('form input[required], form textarea[required]').forEach(input => {
    input.classList.add('required-highlight');
  });
});