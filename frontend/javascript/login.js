function validateFormInputs(){
    const email = document.forms["login"]["email"].value;
    const password = document.forms["login"]["password"].value;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if(email == "" || password == "")
    {
        alert("Both fields must be filled");
        return false;
    }else if(!emailRegex.test(email)){
        alert("Type a valid email");
        return false;
    }else{
        return true;
    }
}

function redirectUserToPortfolioWhenLoginConfirmed(){

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
            return false;
        }
    })
}

function main(){
    if(validateFormInputs() == true){
        redirectUserToPortfolioWhenLoginConfirmed();
    }
}