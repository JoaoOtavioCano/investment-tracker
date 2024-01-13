 let menuIsOpen = false
 
 function openAndCloseMenu(){
    menu = document.getElementById('menu');

    if (menuIsOpen === false){
        menu.style.visibility = "visible";

        menuIsOpen = true;
    }
    else {
        menu.style.visibility = "hidden";

        menuIsOpen = false;
    }
}

