export function checkAuthenticationKeyExists(response){
   console.log("checkAuthenticationKeyExists" + response.statusText);

   if(response.statusText == 'User not authenticated'){
      let redirectPath = '/login';

      window.location.href = redirectPath;
   }
}