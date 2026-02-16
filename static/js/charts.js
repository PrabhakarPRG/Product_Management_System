const ctx = document.getElementById("salesChart");

new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        datasets: [{
            label: "Sales ₹",
            data: [12000, 18000, 15000, 22000, 30000, 25000],
            backgroundColor: "#ff7a00"
        }]
    }
});
