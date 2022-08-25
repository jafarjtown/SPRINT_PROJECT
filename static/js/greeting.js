const greeting_p = document.getElementById('greeting_p')
function greet(){
    const date = new Date()
    let greeting = 'Good '
    let hour = date.getHours() 
    let am_pm = 'am'
    if(hour > 12 & hour < 16){
        greeting += 'Afternoon 🌞'
    }
    else if(hour > 15 & hour < 19){
        greeting += 'Evening 🌜 '
    }
    else{
        greeting += 'Morning 🐓 '
    }
    greeting_p.innerText = greeting
}
greet()