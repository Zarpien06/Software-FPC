document.getElementById('menuToggle').addEventListener('click', function() {
    document.getElementById('sidebar').style.width = '250px';
    document.querySelector('.top-bar').style.marginLeft = '250px';
});

document.getElementById('closeSidebar').addEventListener('click', function() {
    document.getElementById('sidebar').style.width = '0';
    document.querySelector('.top-bar').style.marginLeft = '0';
});