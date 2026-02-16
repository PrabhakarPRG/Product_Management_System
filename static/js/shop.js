document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll(".add-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function () {

            const productId = this.getAttribute("data-id");

            fetch("/cart/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Product added to cart!");
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });

        });
    });

});
