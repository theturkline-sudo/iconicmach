// assets/js/animations.js

document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
});

function initScrollAnimations() {
    const reveals = document.querySelectorAll('.reveal');

    const revealOptions = {
        threshold: 0.15, // 15% of the element must be visible
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, revealOptions);

    reveals.forEach(reveal => {
        revealOnScroll.observe(reveal);
    });
}
