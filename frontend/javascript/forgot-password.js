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
    .then((response) => {
        if (response.status == 500){
            errorUserNotFound()
        }else if (response.status != 200){
            successAlert();
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

    document.getElementsByClassName("email")[0].children[0].innerText = "";
    document.getElementsByClassName("email")[0].style.border = "0px";
    document.getElementById("email").style.border = "0px";

    document.getElementsByClassName("invalid-user")[0].style.display = "none"

}

function validateFormInputs(){
    const email = document.forms["forgotpassword"]["email"].value;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let errorOccurred = false;

    if (email == ""){
        errorMessage("email", "Must be field!");
        errorOccurred = true;
    }else if (!emailRegex.test(email)){
        errorMessage("email", "Type a valid email!");
        errorOccurred = true;
    }

    return !errorOccurred;
}

function errorUserNotFound(){
    errorMessageDiv = document.getElementsByClassName("invalid-user")[0];

    errorMessageDiv.style.display = "flex";
}

function successAlert(){
    alert = document.getElementById("email-sent-alert");

    alert.style.display = "flex";

    setTimeout(() => { alert.style.display = "none"; }, 3000);
}

function cleanInputField(inputId){
    inputField = document.getElementById(inputId);

    inputField.value = "";
}

function main(){
    removeErrorMessages();

    if(validateFormInputs()){
        confirmEmailAddress();
        cleanInputField("email");
    }
}