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
