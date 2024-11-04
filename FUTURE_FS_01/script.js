// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        themeToggle.innerText = 'Switch to Light Mode';
    } else {
        themeToggle.innerText = 'Switch to Dark Mode';
    }
});
