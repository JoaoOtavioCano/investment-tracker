function confirmNewPassword(){
    const code = document.forms.newpassword.code.value
    const newPassword = document.forms.newpassword.new_password.value

    const account = {
        "code": code,
        "new_password": newPassword,
    }

    const jsonString = JSON.stringify(account);

    fetch('/newpassword', { 
        method: 'POST',
        body: jsonString
    })
}