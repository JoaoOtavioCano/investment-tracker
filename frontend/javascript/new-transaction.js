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