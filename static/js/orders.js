// STATUS UPDATE (ADMIN)
document.querySelectorAll(".updateStatus").forEach(select => {
  select.addEventListener("change", () => {
    fetch("/admin/orders/update-status", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        order_id: select.dataset.id,
        status: select.value
      })
    }).then(() => {
      select.closest("tr").querySelector(".badge").className =
        "badge " + select.value;
      select.closest("tr").querySelector(".badge").innerText =
        select.value;
    });
  });
});

// FILTER
document.getElementById("statusFilter").addEventListener("change", function(){
  document.querySelectorAll("#ordersTable tr").forEach(row=>{
    row.style.display =
      !this.value || row.dataset.status === this.value ? "" : "none";
  });
});

