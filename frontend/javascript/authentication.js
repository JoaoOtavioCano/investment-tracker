export function checkAuthenticationKeyExists(response){
   if (reponse.status === 500){
      response.text().then((text) => {
         if(text == 'User not authenticated'){
            let redirectPath = '/login';
      
            window.location.href = redirectPath;
         }
      })
   }
}