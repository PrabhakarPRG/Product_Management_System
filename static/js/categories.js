function openCategoryModal() {
  document.getElementById("categoryModal").style.display = "flex";
}

function closeCategoryModal() {
  document.getElementById("categoryModal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  const saveBtn = document.getElementById("saveCategory");

  if (saveBtn) {
    saveBtn.onclick = () => {
      const form = document.getElementById("categoryForm");
      const data = new FormData(form);

      fetch("/admin/categories/add", {
        method: "POST",
        body: data
      })
      .then(res => res.json())
      .then(res => {
        if (res.success) {
          location.reload();
        } else {
          alert(res.error || "Failed to add category");
        }
      })
      .catch(() => alert("Server error"));
    };
  }
});
