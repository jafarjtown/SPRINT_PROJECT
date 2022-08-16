const orderBtns = document.querySelectorAll('[data-open-order]')
orderBtns.forEach(btn => {
    const catItem = btn.parentElement.parentElement
    const modal = catItem.querySelector('.cat-item-modal-wrp')
    btn.addEventListener('click', ()=> { 
        const close = catItem.querySelector('.cat-item-modal-close')
        modal.style.display = 'flex'
        close.addEventListener('click', ()=> modal.style.display = 'none')

    })
    const form = modal.querySelector('form')
    let price_input = form.querySelector('#price')
    let org_price = price_input.value.slice(1,);
    let quantity_input = form.querySelector('#quantity')
    console.log(price_input.value, quantity_input.value)
    quantity_input.addEventListener('change', ()=> {
        
        console.log(org_price)
        console.log(quantity_input.value)
        price_input.value = `N${(org_price * quantity_input.value)}`
    })
    
})