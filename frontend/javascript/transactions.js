function getTransactions(){
    fetch('/gettransactions', { method: 'GET' })
        .then((response) => response.json())
        .then((json) => {
            for(let i = 0; i < json.length; i++){
                addRow(json[i]);
            }
        })
}

function addRow(transaction){
    let date;
    let asset;
    let quantity;
    let price;
    let total;

    let td_date = document.createElement("td");
    let td_asset = document.createElement("td");
    let td_quantity = document.createElement("td");
    let td_price = document.createElement("td");
    let td_total = document.createElement("td");

    let tr = document.createElement("tr");

    let table = document.getElementById("transactions-table");

    date = document.createTextNode(transaction["date_time"]);
    asset = document.createTextNode(transaction["asset"]);
    quantity = document.createTextNode(transaction["quantity"]);
    price = document.createTextNode(transaction["price"]);
    total = document.createTextNode(transaction["total"]);
    
    td_date.appendChild(date);
    td_asset.appendChild(asset);
    td_quantity.appendChild(quantity);
    td_price.appendChild(price);
    td_total.appendChild(total);

    tr.appendChild(td_date);
    tr.appendChild(td_asset);
    tr.appendChild(td_quantity);
    tr.appendChild(td_price);
    tr.appendChild(td_total);

    table.appendChild(tr);
}

function openModal() {
    let modal = document.getElementById("new-transaction")
    let overlay = document.getElementById("overlay");

    overlay.style.display = 'block';
    modal.style.display = 'block';
}

function closeModal(){
    let modal = document.getElementById("new-transaction")
    let overlay = document.getElementById("overlay");

    overlay.style.display = '';
    modal.style.display = '';
}

function main(){
    getTransactions()
}

main()