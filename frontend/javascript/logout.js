function logOut(){
    fetch('/logout', {
        method: 'POST'
    }).then((response) => {
        if(response.status === 200){
            const redirectPath = "/login";
            
            window.location.href = redirectPath;
        }else{
            return false;
        }
    })
}