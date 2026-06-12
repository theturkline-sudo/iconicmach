// assets/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initThemeToggle();
    initLanguageSwitcher();
});

function initNavigation() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            
            // Animate hamburger
            const spans = menuToggle.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
}

function initThemeToggle() {
    const themeBtn = document.getElementById('theme-toggle');
    
    // Check local storage or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon(true);
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            if (isDark) {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                updateThemeIcon(false);
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                updateThemeIcon(true);
            }
        });
    }
}

function updateThemeIcon(isDark) {
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.innerHTML = isDark ? '☀️' : '🌙';
    }
}

function initLanguageSwitcher() {
    // Current setup uses distinct directories for lang (/ar/, /en/)
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
        langBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const currentPath = window.location.pathname;
            
            if (currentPath.includes('/en/')) {
                window.location.href = currentPath.replace('/en/', '/ar/');
            } else if (currentPath.includes('/ar/')) {
                window.location.href = currentPath.replace('/ar/', '/en/');
            } else {
                // Root fallback
                window.location.href = '/en/';
            }
        });
    }
}
