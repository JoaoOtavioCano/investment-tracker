function validateFormInputs(){
    const email = document.forms["login"]["email"].value;
    const password = document.forms["login"]["password"].value;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    let errorOccurred = false;

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

function tryToLogin(){

    email =document.forms.login.email.value
    password =document.forms.login.password.value

    const requestData = {
        email: email,
        password: password,
    };
    

    const jsonString = JSON.stringify(requestData);

    fetch('/login', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonString,
    })
    .then((response) => {

        if (response.status === 200){

            response.json().then((json) => {
                localStorage.setItem('user', json.user);
            })

            const redirectPath = "/portfolio";

            window.location.href = redirectPath;
        }else{
            errorInvalidCredentials();
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
    fields = ["email", "password"];

    for (field in fields){
        document.getElementsByClassName(fields[field])[0].children[0].innerText = "";
        document.getElementsByClassName(fields[field])[0].style.border = "0px";
        document.getElementById(fields[field]).style.border = "0px";
    }

    errorMessageDiv = document.getElementsByClassName("fail-login")[0];

    errorMessageDiv.style.display = "none";

}

function errorInvalidCredentials(){
    errorMessageDiv = document.getElementsByClassName("fail-login")[0];

    errorMessageDiv.style.display = "flex";
}

function main(){
    removeErrorMessages();

    if(validateFormInputs()){
        tryToLogin();
    }
}