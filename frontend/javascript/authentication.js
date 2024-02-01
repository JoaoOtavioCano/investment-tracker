export function checkAuthenticationKeyExists(response){

   if (response.status === 500){
      response.text().then((text) => {
         console.log(text);
         if(text == 'User not authenticated'){
            console.log("entrou");
            let redirectPath = '/login';
      
            window.location.href = redirectPath;
         }
      })
   }
}