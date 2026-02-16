function addToCart(productId) {
    fetch("/cart/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Added to cart!");
        } else {
            alert("Failed to add");
        }
    });
}


document.getElementById("checkoutBtn").addEventListener("click", function () {

    fetch("/create-payment", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ amount: document.getElementById("totalAmount").value })
    })
    .then(res => res.json())
    .then(data => {

        var options = {
            key: data.razorpay_key,
            amount: data.amount,
            currency: "INR",
            order_id: data.order_id,

            handler: function (response) {

                fetch("/verify-payment", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        razorpay_payment_id: response.razorpay_payment_id,
                        razorpay_order_id: response.razorpay_order_id,
                        razorpay_signature: response.razorpay_signature,
                        order_id: 1,  // Replace dynamically
                        amount: data.amount
                    })
                })
                .then(res => res.json())
                .then(result => {
                    if (result.status === "success") {
                        alert("Payment Successful!");
                        window.location.href = "/orders";
                    } else {
                        alert("Payment Failed!");
                    }
                });
            }
        };

        var rzp = new Razorpay(options);
        rzp.open();
    });
});
