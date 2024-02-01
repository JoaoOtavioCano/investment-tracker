function logOut(){
    fetch('/logout', {
        method: 'POST'
    }).then(() => {
        let redirectPath = '/login';
      
        window.location.href = redirectPath;
    })
}