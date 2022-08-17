// const all_toolkit = document.querySelectorAll('.admin-sets-list')

// all_toolkit.forEach(toolkit => toolkit.classList.toggle('hide'))
const toggler = document.querySelector('[data-toggler]')
const aside = document.querySelector('[data-aside]')

toggler.addEventListener('click', ()=>{
    aside.classList.toggle('show')
})

document.querySelector('[admin-sets]').addEventListener('click', ()=>{
    document.querySelector('[admin-sets-view]').classList.toggle('show')
})
document.querySelector('[admin-kt]').addEventListener('click', ()=>{
    document.querySelector('[admin-kt-view]').classList.toggle('show')
})

