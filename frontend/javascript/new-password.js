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
    .then((response) => {
        if (response.status == 500){
            errorInvalidCode();
        }
    })
}

function errorMessage(field, message){

    errorMessageDiv = document.getElementsByClassName(field)[0];
    errorMessageSpan = document.getElementsByClassName(field)[0].children[0];
    inputField = document.getElementById(field);

    inputField.style.border = "2px solid red";

    errorMessageDiv.style.border = "2px solid red"

    errorMessageSpan.innerText = message;
}

function removeErrorMessages(){
    fields = ["code", "new_password"];

    for (field in fields){
        document.getElementsByClassName(fields[field])[0].children[0].innerText = "";
        document.getElementsByClassName(fields[field])[0].style.border = "0px";
        document.getElementById(fields[field]).style.border = "0px";
    }

    errorMessageDiv = document.getElementsByClassName("invalid-code")[0];

    errorMessageDiv.style.display = "none";

}

function validateFormInputs(){
    const code = document.forms.newpassword.code.value;
    const newPassword = document.forms.newpassword.new_password.value;

    let errorOccurred = false;

    if (code == ""){
        errorMessage("code", "Must be field!");
        errorOccurred = true;
    } 
    if (newPassword == ""){
        errorMessage("new_password", "Must be field!");
        errorOccurred = true;
    }

    return !errorOccurred;
}

function errorInvalidCode(){
    errorMessageDiv = document.getElementsByClassName("invalid-code")[0];

    errorMessageDiv.style.display = "flex";
}

function main(){
    removeErrorMessages();

    if(validateFormInputs()){
        confirmNewPassword();
    }
}