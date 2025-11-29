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

const filterSelect = document.getElementById('status-filter');
if (filterSelect) {
    filterSelect.addEventListener('change', () => {
        const filterValue = filterSelect.value.toLowerCase();
        document.querySelectorAll('.dashboard-table tbody tr').forEach(row => {
            const statusCell = row.querySelector('.status-cell');
            if(!statusCell) return;
            if(statusCell.textContent.toLowerCase().includes(filterValue) || filterValue === 'all') {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}