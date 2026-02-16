function deleteProduct(id){
  if(!confirm("Delete this product?")) return;

  fetch(`/admin/products/delete/${id}`, { method:'POST' })
    .then(() => {
      document.getElementById(`row-${id}`).style.opacity = 0;
      setTimeout(() => {
        document.getElementById(`row-${id}`).remove();
      }, 300);
    });
}

function openProductModal(){
  const modal = document.getElementById('productModal');
  modal.style.display = 'flex';
}

function closeProductModal(){
  document.getElementById('productModal').style.display = 'none';
}

function closeOnOverlay(e){
  if(e.target.classList.contains('modal-overlay')){
    closeProductModal();
  }
}
