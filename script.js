document.addEventListener("DOMContentLoaded", () => {
    const menuBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    const mobileLinks = document.querySelectorAll(".mobile-link");

    // Toggle dynamic mobile drawer systems
    menuBtn.addEventListener("click", () => {
        mobileMenu.classList.toggle("show");
    });

    mobileLinks.forEach(link => {
        link.addEventListener("click", () => {
            mobileMenu.classList.remove("show");
        });
    });
});

// Securely initiates payment handling loop flow using Razorpay standard checkout layers
function payNow(planId) {
    fetch('/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan_id: planId })
    })
    .then(response => response.json())
    .then(order => {
        if (order.error) {
            alert('Initialization Error: ' + order.error);
            return;
        }

        const options = {
            "key": window.RAZORPAY_KEY_ID,
            "amount": order.amount,
            "currency": order.currency,
            "name": "IRON PULSE CLUB",
            "description": `Premium Membership Plan: ${planId.toUpperCase()}`,
            "order_id": order.id,
            "callback_url": window.VERIFY_URL, // Automatically triggers POST form submit handle back to Flask server endpoints
            "prefill": {
                "name": "Elite Athlete",
                "email": "athlete@ironpulse.com",
                "contact": "9999999999"
            },
            "theme": {
                "color": "#f59e0b" // Accent matching amber tint colors
            }
        };

        const rzp = new Razorpay(options);
        rzp.open();
    })
    .catch(err => {
        console.error("Order Creation Request Interrupted: ", err);
        alert("An unexpected error occurred. Please verify connectivity layers.");
    });
}
