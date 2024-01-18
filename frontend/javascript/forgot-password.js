function confirmEmailAddress(){
    const email = document.forms.forgotpassword.email.value

    const account = {
        "email": email,
    }

    const jsonString = JSON.stringify(account);

    fetch('/forgotpassword', { 
        method: 'POST',
        body: jsonString
    })
}