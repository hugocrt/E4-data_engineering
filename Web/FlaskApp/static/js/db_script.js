const yearRangeForm = document.getElementById('yearRangeForm');
const sortingForm = document.getElementById('sortingForm');
const durationRangeForm = document.getElementById('durationRangeForm');
const minYearSelect = document.getElementById('min_year');
const maxYearSelect = document.getElementById('max_year');
const minDurationSelect = document.getElementById('min_duration');
const maxDurationSelect = document.getElementById('max_duration');
const sortOrderSelect = document.getElementById('sort_order');

minYearSelect.addEventListener('change', () => {
    yearRangeForm.submit();
});

maxYearSelect.addEventListener('change', () => {
    yearRangeForm.submit();
});

minDurationSelect.addEventListener('change', () => {
    durationRangeForm.submit();
});

maxDurationSelect.addEventListener('change', () => {
    durationRangeForm.submit();
});

sortOrderSelect.addEventListener('change', () => {
    sortingForm.submit();
});

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const sectionContent = section.querySelector('.section-content');
    const arrow = section.querySelector('.arrow');

    // Toggle the "active" class on the section
    section.classList.toggle('active');

    // Rotate the arrow based on the "active" class
    arrow.style.transform = section.classList.contains('active') ? 'rotateX(180deg)' : 'rotateX(0deg)';

    // Toggle the visibility of the section content
    sectionContent.style.display = (section.classList.contains('active')) ? 'block' : 'none';
}



