document.addEventListener("DOMContentLoaded", () => {
    const cartButtons = document.querySelectorAll(".add-to-cart");

    cartButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const url = button.getAttribute("href");

            fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        // Update the cart count in the navbar
                        const cartBadge = document.querySelector(".cart-badge");
                        if (cartBadge) {
                            cartBadge.textContent = data.cart_count;
                        }

                        // Show feedback to the user
                        showToast("Item added to cart!"); // Use a toast instead of alert
                    }
                })
                .catch((error) => console.error("Error adding to cart:", error));
        });
    });

    // Function to display a toast message
    function showToast(message) {
        // Create a toast element
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = message;

        // Style the toast (you can move this to CSS)
        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.backgroundColor = "#28a745";
        toast.style.color = "white";
        toast.style.padding = "10px 20px";
        toast.style.borderRadius = "5px";
        toast.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
        toast.style.zIndex = "1000";

        // Append the toast to the body
        document.body.appendChild(toast);

        // Remove the toast after 3 seconds
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 3000);
    }
});
