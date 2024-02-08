function showImage(row){
    // Create a new <td> element
    var newTd = document.createElement('td');
    newTd.id = 'delete-transaction';
    
    // Create a <span> element for the icon
    var span = document.createElement('span');
    span.className = 'material-symbols-outlined';
    span.textContent = 'delete_forever';
    span.onclick = () => { console.log("click")}
    
    // Append the <span> to the <td>
    newTd.appendChild(span);
    
    // Append the new <td> to the row
    row.appendChild(newTd);
}

function removeImage(row) {
    // Get the last child of the row, which is the <td> with the icon
    var lastChild = row.lastElementChild;
    
    // Remove the last child from the row
    row.removeChild(lastChild);
}