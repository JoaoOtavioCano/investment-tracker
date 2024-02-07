function deleteAccount() {
    fetch('/deleteaccount', { 
        method: 'POST',
    })
    .then(() => {
        let redirectPath = '/login';
        
        window.location.href = redirectPath;
    })
}

function areUSureModal() {
    modal = document.getElementById("delete-account-modal");
    overlay = document.getElementById("overlay");

    modal.style.visibility = "visible";
    overlay.style.display = "flex";
}

function confirmDeletion() {
    deleteAccount();
}

function cancelDeletion() {
    modal = document.getElementById("delete-account-modal");
    overlay = document.getElementById("overlay");

    modal.style.visibility = "hidden";
    overlay.style.display = "none";
}