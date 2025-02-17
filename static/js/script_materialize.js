document.addEventListener('DOMContentLoaded', function () {
    const selectElems = document.querySelectorAll('select');
    M.FormSelect.init(selectElems);
});

var tooltips = document.querySelectorAll('.tooltipped');
M.Tooltip.init(tooltips, {
    position: 'bottom'
});