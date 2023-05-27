//load the page on full screen mode ( function from https://www.w3schools.com/howto/howto_js_fullscreen.asp#:%7E:text=Try%20it%20Yourself%20%C2%BB-,Fullscreen%20Document,-To%20open%20the)

function openFullscreen() {
    let elem = document.querySelector('#PRESENT-presentation')
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
    let theBtn = document.querySelector('#PRESENT-page-1-btn')
    theBtn.classList.add("BASE-hide")
}

// if user exits full screen mode, show button again
function checkFullscreenClose(){
    if (document.fullscreenElement === null) {
        let theBtn = document.querySelector('#PRESENT-page-1-btn')
        theBtn.classList.remove("BASE-hide")
    }
}
window.addEventListener("fullscreenchange", (event) => {
    checkFullscreenClose()
})

// show next page if user presses 'enter'
function changePage(nextOrPrevious){
    let allPages = document.querySelectorAll('.PRESENT-page');
    let currentPage;
    allPages.forEach(page => {
        if (!page.matches('.BASE-hide')) {
            currentPage = parseInt(page.dataset.pagenr)
            page.classList.add('BASE-hide')
        }
    })
    // dont forget to include the logic to check if first and last page to avoid problems
    let nextPageNr;
    if (nextOrPrevious === "next") {
        nextPageNr = currentPage + 1
    } else {
        nextPageNr = currentPage - 1
    }
    nextPageNr = nextPageNr.toString()
    let nextPage = document.querySelector(`[data-pagenr='${nextPageNr}']`)
    nextPage.classList.remove("BASE-hide")
}

document.addEventListener("keydown", (event) =>{
    if(event.keyCode === 13){
        changePage("next")
    }
})