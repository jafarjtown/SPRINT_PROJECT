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

async function AddToCart(url,q){
    const loading_modal = document.querySelector('.loading-modal')
    loading_modal.querySelector('p').innerText = 'Adding item to cart... please wait'
    loading_modal.style.display = 'flex'
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'content-type': 'application/json'
        },
        body:JSON.stringify({
            quantity: q
        })
    })
    const data = await response.json()
    console.log(data)
    if(data.success == true){
        loading_modal.querySelector('p').innerText = 'successfully'
        setTimeout(()=>{
            loading_modal.style.display = 'none'
        },1500)
    }else{
        loading_modal.querySelector('p').innerText = 'Error occured... try again'
        setTimeout(()=>{
            loading_modal.style.display = 'none'
        },1500)
    }
}