function createAccount(){
    const name = document.forms.createaccount.name.value
    const email = document.forms.createaccount.email.value
    const password = document.forms.createaccount.password.value

    const account = {
        "name": name,
        "email": email,
        "password": password,
    }

    const jsonString = JSON.stringify(account);

    fetch('/createaccount', { 
        method: 'POST',
        body: jsonString
    })
}