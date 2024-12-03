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

                        // Optionally, show feedback to the user
                        alert("Product added to cart successfully!");
                    }
                })
                .catch((error) => console.error("Error adding to cart:", error));
        });
    });
});
