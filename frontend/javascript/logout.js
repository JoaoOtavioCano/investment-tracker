function logOut(){
    fetch('/logout', {
        method: 'POST'
    })
}