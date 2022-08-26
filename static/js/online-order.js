
const method = document.querySelector('[name="payment_type"]')

method.addEventListener('change', ()=> {
    let typ = method.value
    if(typ === 'O'){
        document.querySelector('.online').classList.add('grid')
    }
    else{
        document.querySelector('.online').classList.remove('grid')
    }
})

const paymentForm = document.getElementById('paystack');
paymentForm.addEventListener("click", payWithPaystack, false);
function payWithPaystack(e) {
  e.preventDefault();

  let handler = PaystackPop.setup({
    key: 'pk_test_3f117b6d04d315b87cbf3602b95d7d19505e2f76', // Replace with your public key
    email: document.getElementById("email-address").value,
    amount: document.getElementById("amount").value * 100,
    ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    // label: "Optional string that replaces customer email"
    onClose: function(){
      alert('Window closed.');
    },
    callback: function(response){
      let message = 'Payment complete! Reference: ' + response.reference;
      paymentSuccessfully(response.reference);
    }
  });

  handler.openIframe();
}

async function paymentSuccessfully(ref){
    const response = await fetch(document.querySelector('#payment-success-url').value, {
        method: 'POST',
        headers:{
            'content-type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        body:JSON.stringify({
            ref,
            delivery_point: document.getElementsByName('delivery_point')[0].value,
            phone_no: document.getElementsByName('phone_number')[0].value,
        })
    })
    const data = await response.json()
    if(data.success = true){
        location.reload()
    }
}