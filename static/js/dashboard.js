const toggler = document.querySelector('[menu-toggler]')
const toggler2 = document.querySelector('[menu-toggler2]')
const aside = document.querySelector('[data-aside]')

toggler.addEventListener('click', ()=>{
    console.log('click')
    aside.classList.toggle('hide_nav')
    aside.classList.remove('show_span')

})
toggler2.addEventListener('click', ()=>{
    console.log('double click')
    aside.classList.toggle('show_span')
})