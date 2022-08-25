const greeting_p = document.getElementById('greeting_p')
function greet(){
    const date = new Date()
    let greeting = 'Good '
    let hour = date.getHours() 
    console.log(hour)
    if(hour > 12 & hour < 16){
        greeting += 'Afternoon 🌞'
    }
    else if(hour > 15 & hour < 21){
        greeting += 'Evening 🌜 '
    }
    else if(hour >= 21){
        greeting += 'Night 🌚 '
    }
    else{
        greeting += 'Morning 🐓 '
    }
    greeting_p.innerText = greeting
}
greet()