const yearRangeForm = document.getElementById('yearRangeForm');
    const minYearSelect = document.getElementById('min_year');
    const maxYearSelect = document.getElementById('max_year');
    const sortOrderSelect = document.getElementById('sort_order');

    minYearSelect.addEventListener('change', () => {
        yearRangeForm.submit();
    });

    maxYearSelect.addEventListener('change', () => {
        yearRangeForm.submit();
    });

    sortOrderSelect.addEventListener('change', () => {
        sortingForm.submit();
    });