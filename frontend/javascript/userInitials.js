export function setUserInitials(){
    const initials = getUserInitials()

    document.getElementById('user-initials').innerText = initials;
}

function getUserInitials(){
    const user = localStorage.getItem('user');

    return `${user[0]}${user[1]}`;
}