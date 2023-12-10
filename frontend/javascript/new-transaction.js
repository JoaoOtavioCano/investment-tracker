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
    inputs = document.getElementsByTagName("input");

    for(let i = 0; i < inputs.length; i++){
        if(inputs[i].value == ""){
            alert(`${inputs[i].name} field must be filled`)
            return false;
        }
    }

    return true
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

listenEventRecalculateTotal()