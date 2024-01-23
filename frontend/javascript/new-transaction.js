function clickBuy(){
    document.getElementById("buy").style.backgroundColor = "#00FD8F";
    document.getElementById("sell").style.backgroundColor = "";

    document.getElementById("buy/sell").value = 'buy';
}

function clickSell(){
    document.getElementById("buy").style.backgroundColor = "";
    document.getElementById("sell").style.backgroundColor = "red";

    document.getElementById("buy/sell").value = 'sell';
}

function validateFormInputs(){
    const buyOrSell = document.forms.newtransaction["buy/sell"].value;
    const asset = document.forms.newtransaction.asset.value;
    const date = document.forms.newtransaction.date.value;
    const price = document.forms.newtransaction.price.value;
    const quantity = document.forms.newtransaction.quantity.value;

    let errorOccurred = false;

    if (buyOrSell == ""){
        errorMessage("buy-sell", "Must be field!");
        errorOccurred = true;
    }
    if (asset == ""){
        errorMessage("asset", "Must be field!");
        errorOccurred = true;
    }
    if (date == ""){
        errorMessage("date", "Must be field!");
        errorOccurred = true;
    }
    if (price == ""){
        errorMessage("price", "Must be field!");
        errorOccurred = true;
    } 
    if (quantity == ""){
        errorMessage("quantity", "Must be field!");
        errorOccurred = true;
    }

    return !errorOccurred;
}

function errorMessage(field, message){

    errorMessageDiv = document.getElementsByClassName(field)[0];
    errorMessageSpan = document.getElementsByClassName(field)[0].children[0];

    if(field != "buy-sell"){
        inputField = document.getElementById(field);
    }else{
        inputField = document.getElementById("buy");
        inputField.style.border = "2px solid red";
        inputField = document.getElementById("sell");
    }

    inputField.style.border = "2px solid red";

    errorMessageSpan.innerText = message;

    errorMessageDiv.style.display = "flex";
}

function removeErrorMessages(){
    fields = ["asset", "date", "price", "quantity"];

    for (field in fields){
        document.getElementsByClassName(fields[field])[0].children[0].innerText = "";
        document.getElementsByClassName(fields[field])[0].style.display = "none";
        document.getElementById(fields[field]).style.border = "0px";
    }

    document.getElementsByClassName("buy-sell")[0].children[0].innerText = "";
    document.getElementsByClassName("buy-sell")[0].style.display = "none";
    document.getElementById("buy").style.border = "0px";    
    document.getElementById("sell").style.border = "0px";    
}

function calculateTotal(){
    const price = document.getElementById("price").value;
    const quantity = document.getElementById("quantity").value;

    const total = price * quantity;

    document.getElementById("total").textContent = "TOTAL: $" + total.toFixed(2).toString();
}

function listenEventRecalculateTotal(){
    document.getElementById("price").addEventListener("input", () => {
        calculateTotal();
    })
    
    document.getElementById("quantity").addEventListener("input", () => {
        calculateTotal();
    })
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

function postTransaction(){
    const operation = document.forms.newtransaction['buy/sell'].value
    const asset = document.forms.newtransaction.asset.value
    const date = document.forms.newtransaction.date.value
    const price = document.forms.newtransaction.price.value
    const quantity = document.forms.newtransaction.quantity.value
    const type = document.forms.newtransaction.type.value

    transaction = {
        "operation": operation,
        "asset": asset,
        "date": date,
        "price": price,
        "quantity": quantity,
        "type": type,
    }

    const jsonString = JSON.stringify(transaction);

    fetch('/newtransaction', { 
        method: 'POST',
        body: jsonString
    })
}

function newTransaction(){
    removeErrorMessages();

    if (validateFormInputs()){
        postTransaction();
        closeModal();
        
    }
}

listenEventRecalculateTotal()