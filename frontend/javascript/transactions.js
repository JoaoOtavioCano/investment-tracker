import { checkAuthenticationKeyExists } from './authentication.js';
import { setUserInitials } from './userInitials.js';
import { gotToTheEndOfTheScroll } from './transaction-pagination.js';

let frameNumber = 0;
let allTransactionsGot = false;

export function getTransactions(){

    if (!allTransactionsGot){
        fetch(`/gettransactions?frame=${frameNumber}`, { method: 'GET'})
            .then((response) => {
                checkAuthenticationKeyExists(response);

                return response.json();
            })
            .then((json) => {
                for(let i = 0; i < json.length; i++){
                    addRow(json[i]);
                }

                if (json.length < 20){
                    allTransactionsGot = true;
                }
            })

        frameNumber++;
    }
}

function addRow(transaction){
    let date;
    let asset;
    let operation;
    let quantity;
    let price;
    let total;

    let td_date = document.createElement("td");
    let td_asset = document.createElement("td");
    let td_operation = document.createElement("td");
    let td_quantity = document.createElement("td");
    let td_price = document.createElement("td");
    let td_total = document.createElement("td");

    let tr = document.createElement("tr");

    let table = document.getElementById("transactions-table");

    date = document.createTextNode(transaction["date_time"]);
    asset = document.createTextNode(transaction["asset"]);
    operation = document.createTextNode(transaction["operation"]);
    quantity = document.createTextNode(transaction["quantity"]);
    price = document.createTextNode(transaction["price"]);
    total = document.createTextNode(transaction["total"]);

    td_date.className = "date";
    td_asset.className = "asset";
    td_operation.className = "operation";
    td_quantity.className = "quantity";
    td_price.className = "price";
    td_total.className = "total";
    
    td_date.appendChild(date);
    td_asset.appendChild(asset);
    td_operation.appendChild(operation);
    td_quantity.appendChild(quantity);
    td_price.appendChild(price);
    td_total.appendChild(total);

    tr.appendChild(td_date);
    tr.appendChild(td_asset);
    tr.appendChild(td_operation);
    tr.appendChild(td_quantity);
    tr.appendChild(td_price);
    tr.appendChild(td_total);

    table.appendChild(tr);
}

function main(){
    setUserInitials();
    getTransactions();
    gotToTheEndOfTheScroll();
}

main();
