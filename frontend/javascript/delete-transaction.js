function showImage(row){
    // Create a new <td> element
    let extraTd = row.lastElementChild;
    
    // Create a <span> element for the icon
    let span = document.createElement('span');
    span.className = 'material-symbols-outlined';
    span.textContent = 'delete_forever';
    span.onclick = () => {
            const transactionId = row.className.replace("id", "");
            console.log(transactionId) 
            deleteTransaction(transactionId);
        }
    
    // Append the <span> to the <td>
    extraTd.appendChild(span);
}

function removeImage(row) {
    // Get the last child of the row, which is the <td> with the icon
    let lastChild = row.lastElementChild;

    let lastChildSpan = lastChild.lastElementChild;
    
    // Remove the last child from the row
    lastChild.removeChild(lastChildSpan);
}

function deleteTransaction(transactionId){
    const transaction = {
        "transactionId": transactionId,
    }

    const jsonString = JSON.stringify(transaction);

    fetch("/deletetransaction", {
        method: "POST",
        body: jsonString
    })
    .then((response) => {
        if (response.status == 200){
            location.reload();
        }
    })
}