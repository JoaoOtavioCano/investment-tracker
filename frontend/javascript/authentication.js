export function checkAuthenticationKeyExists(response){
   if(response.statusText == 'User not authenticated'){
      let redirectPath = '/login';

      window.location.href = redirectPath;
   }
}