// const all_toolkit = document.querySelectorAll('.admin-sets-list')

// all_toolkit.forEach(toolkit => toolkit.classList.toggle('hide'))


document.querySelector('[admin-sets]').addEventListener('click', ()=>{
    document.querySelector('[admin-sets-view]').classList.toggle('show')
})
document.querySelector('[admin-kt]').addEventListener('click', ()=>{
    document.querySelector('[admin-kt-view]').classList.toggle('show')
})