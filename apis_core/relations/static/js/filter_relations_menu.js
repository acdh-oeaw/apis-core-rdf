document.addEventListener('DOMContentLoaded', function() {
    const relationList = document.getElementById('relationList');
    const filterInput = document.getElementById('relationFilter');
    const items = relationList.getElementsByClassName('relation-item');

    filterInput.style.display = items.length > 10 ? 'block' : 'none';

    function filterItems() {
        const filter = filterInput.value.toLowerCase();
        for (let item of items) {
            const text = item.textContent.toLowerCase();
            if (text.includes(filter)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        }
    }

    filterInput.addEventListener('input', filterItems);
});
