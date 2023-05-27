// show next poll page
function changePage(nextOrPrevious) {
    event.preventDefault()
    let allPages = document.querySelectorAll('.POLL-page');
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