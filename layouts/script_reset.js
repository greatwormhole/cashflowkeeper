
const reset_button=document.getElementById('reset_button')
const reset_before=document.querySelector('.reset')
const reset_after=document.querySelector('.reset_done')

console.log(reset_before)

reset_button.addEventListener('click', (event) => {
    reset_before.style.display = 'none';
    reset_after.style.display = 'flex';
})
  