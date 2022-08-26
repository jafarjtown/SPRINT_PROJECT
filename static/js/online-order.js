
const method = document.querySelector('[name="method"]')

method.addEventListener('change', ()=> {
    let typ = method.value
    if(typ === 'O'){
        document.querySelector('.online').classList.add('grid')
    }
    else{
        document.querySelector('.online').classList.remove('grid')
    }
})