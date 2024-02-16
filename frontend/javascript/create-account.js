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

    cleanInputFields();

    fetch('/createaccount', { 
        method: 'POST',
        body: jsonString
    })
    .then((response) => {
        if (response.status == 200){
            accountCreatedAlert();
            setTimeout(() => { 
                const redirectPath = "/login";

                window.location.href = redirectPath; 
            }, 2000);
        } else {
            errorMessage("email", response.statusText);
        }
    })
}

function errorMessage(field, message){

    errorMessageDiv = document.getElementsByClassName(field)[0];
    errorMessageSpan = document.getElementsByClassName(field)[0].children[0];
    inputField = document.getElementById(field);

    inputField.style.border = "2px solid red";

    errorMessageDiv.style.border = "2px solid red";

    errorMessageSpan.innerText = message;
}

function removeErrorMessages(){
    fields = ["name", "email", "password"];

    for (field in fields){
        document.getElementsByClassName(fields[field])[0].children[0].innerText = "";
        document.getElementsByClassName(fields[field])[0].style.border = "0px";
        document.getElementById(fields[field]).style.border = "0px";
    }
}

function validateFormInputs(){
    const name = document.forms.createaccount.name.value;
    const email = document.forms.createaccount.email.value;
    const password = document.forms.createaccount.password.value;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;


    let errorOccurred = false;

    if (name == ""){
        errorMessage("name", "Must be field!");
        errorOccurred = true;
    } 
    if (email == ""){
        errorMessage("email", "Must be field!");
        errorOccurred = true;
    }else if (!emailRegex.test(email)){
        errorMessage("email", "Type a valid email!");
        errorOccurred = true;
    }
    if (password == ""){
        errorMessage("password", "Must be field!");
        errorOccurred = true;
    }

    return !errorOccurred;
}

function accountCreatedAlert(){
    alert = document.getElementById("account-created-alert");

    alert.style.display = "flex";
}

function removeAccountCreatedAlert(){
    alert = document.getElementById("account-created-alert");

    alert.style.display = "none";
}

function cleanInputFields(){
    const name = document.forms.createaccount.name
    const email = document.forms.createaccount.email
    const password = document.forms.createaccount.password

    name.value = ""
    email.value = ""
    password.value = ""
}

function main(){
    removeErrorMessages();
    removeAccountCreatedAlert();

    if(validateFormInputs()){
        createAccount();
    }
}