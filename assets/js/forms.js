// assets/js/forms.js

document.addEventListener('DOMContentLoaded', () => {
    initForms();
});

function initForms() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Basic Validation
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            
            if (!name || !email || !message) {
                alert('Please fill in all required fields.');
                return;
            }

            // Handle submission state
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = 'Sending...';
            submitBtn.disabled = true;

            try {
                // Collect form data
                const formData = new FormData(contactForm);
                const data = Object.fromEntries(formData.entries());

                // Post to Cloudflare Worker Endpoint
                const response = await fetch('/api/submit-inquiry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    alert('Thank you! Your message has been sent successfully.');
                    contactForm.reset();
                } else {
                    alert('Something went wrong. Please try again later.');
                }
            } catch (error) {
                console.error('Form submission error:', error);
                alert('An error occurred. Please try again.');
            } finally {
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}
