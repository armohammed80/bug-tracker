// Show a "form submitted" alert
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
        alert("Your changes have been submitted!");
    });
});

// Live character count for textareas
document.querySelectorAll('textarea').forEach(textarea => {
    const counter = document.createElement('small');
    counter.style.display = 'block';
    counter.style.marginTop = '0.25rem';
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);

    textarea.addEventListener('input', () => {
        counter.textContent = `${textarea.value.length} characters`;
    });
});