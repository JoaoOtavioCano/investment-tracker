export function checkAuthenticationKeyExists(response){
   console.log(response.status);

   if (response.status === 500){
      response.text().then((text) => {
         console.log(text);
         if(text == 'User not authenticated'){
            let redirectPath = '/login';
      
            window.location.href = redirectPath;
         }
      })
   }
}