// FIND the button by its id
const themeToggle = document.querySelector('#theme-toggle');

// LISTEN for a click
themeToggle.addEventListener('click', () => {
    // CHANGE: flip the 'dark' class on <body>
    document.body.classList.toggle('dark');
    
    // Swap the icon to match the mode
    const isDark = document.body.classList.contains('dark');
    themeToggle.textContent = isDark ? '☀️' : '🌙'; 
});
// FIND the button by its id
const toTop = document.querySelector('#to-top');

// LISTEN for scrolling
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        toTop.classList.add('show');
    } else {
        toTop.classList.remove('show');
    }
});

// Click -> glide back to the top
toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
// FIND every element marked with class "reveal"
const revealItems = document.querySelectorAll('.reveal');

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) { // when it enters the screen
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target); // animate once, then stop
        }
    });
}, { threshold: 0.15 });

revealItems.forEach((item) => observer.observe(item));
const toTop = document.querySelector('#to-top');

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        toTop.classList.add('show');
    } else {
        toTop.classList.remove('show');
    }
});

toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
