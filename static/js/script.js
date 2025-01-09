document.addEventListener('DOMContentLoaded', function() {
    M.Sidenav.init(document.querySelectorAll('.sidenav'));
});

document.getElementById('toggle-sidebar').addEventListener('click', function () {
    const sidenav = document.getElementById('slide-out');
    const toggleButton = document.getElementById('toggle-sidebar');
    const container = document.getElementsByClassName('container')[0];

    if (sidenav.classList.contains('hidden-sidebar')) {
        sidenav.classList.remove('hidden-sidebar');
        toggleButton.style.left = "340px";
        container.style.width = "calc(100% - 400px)";
        container.style.marginLeft = "400px";
    } else {
        sidenav.classList.add('hidden-sidebar');
        toggleButton.style.left = "50px";
        container.style.width = "90vw";
        container.style.marginLeft = "0px";
    }
});

document.addEventListener('DOMContentLoaded', function () {
    if (window.innerWidth <= 900) {
        document.getElementById('slide-out').style.transform = "translateX(-400px)";
        toggleButton.style.left = "50px";
    }
});

function loadDoc(filename) {
    fetch('/doc/' + filename)
        .then(response => response.text())
        .then(data => {
            document.getElementById('doc-content').innerHTML = data;
            hljs.highlightAll(); 
        })
        .catch(error => {
            document.getElementById('doc-content').innerHTML = "<p class='center-align'>Document not found.</p>";
        });
}