const popupContainer = document.querySelector('.popup-container')
const frmButton = document.querySelector('.frm-btn')


document.querySelectorAll('.open-popup').forEach((item) => {
  item.addEventListener('click', () => {
    popupContainer.style.display = 'flex'
  })
})


frmButton.addEventListener('click', () => {
  popupContainer.style.display = 'none'
})


popupContainer.addEventListener('click', (event) => {
  if (event.target == popupContainer) {
    popupContainer.style.display = 'none'
  }
})
