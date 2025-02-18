document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});

var tooltips = document.querySelectorAll('.tooltipped');
M.Tooltip.init(tooltips, {
    position: 'bottom'
});