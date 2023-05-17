function hideUnhideIfChecked(el_id) {
    let theElement = document.querySelector(`#${el_id}`);
    let theCheckbox = event.target;
    if (theCheckbox.checked){
        theElement.classList.remove("BASE-hide");
    } else {
        theElement.classList.add("BASE-hide");
    }
}
