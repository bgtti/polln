function modalHideUnhide(modal_id){
    event.preventDefault()
    let theModal = document.querySelector(`#${modal_id}`);
    if (theModal.classList.contains("BASE-hide")){
        theModal.classList.remove("BASE-hide");
    } else {
        theModal.classList.add("BASE-hide");
    }
}