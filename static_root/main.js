/**
 * @function modalHideUnhide
 * Toggles the visibility of a modal by adding/removing the "BASE-hide" class.
 * 
 * @param {string} modal_id - The ID of the modal element to toggle.
 * 
 * @example
 * <div class="BASE-modal-container BASE-hide" id="modal_add_question">
 *   <!-- modal content here -->
 *   <a href="javascript:void(0)" role="button" class="btn btn-dark my-2 my-sm-0 BASE-btn BASE-btn-type2"
 *      onclick="modalHideUnhide('modal_add_question'); reloadPage();">Close modal</a>
 * </div>
 */
function modalHideUnhide(modal_id) {
    event.preventDefault()
    let theModal = document.querySelector(`#${modal_id}`);
    if (theModal.classList.contains("BASE-hide")) {
        theModal.classList.remove("BASE-hide");
    } else {
        theModal.classList.add("BASE-hide");
    }
}