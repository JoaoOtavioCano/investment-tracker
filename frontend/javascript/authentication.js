export function checkAuthenticationKeyExists(){
    if (localStorage.authenticationKey == null){
        window.location.href = "/login";
    }
}