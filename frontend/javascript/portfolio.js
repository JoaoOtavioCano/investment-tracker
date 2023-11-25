function getAssets(){
    fetch('/assets', { method: 'GET' })
        .then((response) => response.json())
        .then((json) => {
            for(let i = 0; i < json.length; i++){
                addRow(json[i]);
            }
        })
}

function addRow(assets){
    let type;
    let asset;
    let quantity;
    let avg_price;
    let gain_loss;
    let gain_loss_percent;
    let total;

    let td_type = document.createElement("td");
    let td_asset = document.createElement("td");
    let td_quantity = document.createElement("td");
    let td_avg_price = document.createElement("td");
    let td_gain_loss = document.createElement("td");
    let td_gain_loss_percent = document.createElement("td");
    let td_total = document.createElement("td");

    let tr = document.createElement("tr");

    let table = document.getElementById("assets-table");

    type = document.createTextNode(assets["type"]);
    asset = document.createTextNode(assets["asset"]);
    quantity = document.createTextNode(assets["quantity"]);
    avg_price = document.createTextNode(assets["avg_price"]);
    gain_loss = document.createTextNode(assets["gain_loss"]);
    gain_loss_percent = document.createTextNode(assets["gain_loss_percent"]);
    total = document.createTextNode(assets["total"]);
    
    td_type.appendChild(type);
    td_asset.appendChild(asset);
    td_quantity.appendChild(quantity);
    td_avg_price.appendChild(avg_price);
    td_gain_loss.appendChild(gain_loss);
    td_gain_loss_percent.appendChild(gain_loss_percent);
    td_total.appendChild(total);

    if(Number(assets["gain_loss"]) >= 0){
        td_gain_loss.style.color = "#00FD8F";
        td_gain_loss_percent.style.color = "#00FD8F";
    }else{
        td_gain_loss.style.color = "red";
        td_gain_loss_percent.style.color = "red";
    }

    tr.appendChild(td_type);
    tr.appendChild(td_asset);
    tr.appendChild(td_quantity);
    tr.appendChild(td_avg_price);
    tr.appendChild(td_gain_loss);
    tr.appendChild(td_gain_loss_percent);
    tr.appendChild(td_total);

    table.appendChild(tr);
}

function getIndicators(){
    fetch('/indicators', { method: 'GET' })
        .then((response) => response.json())
        .then((json) => {
            addIndicators(json);
            gainLossIndicatorColor();
        })
}

function addIndicators(indicators){
    let net_worth = indicators["net_worth"];
    let gain_loss = indicators["gain_loss"];
    let price = indicators["price"];

    document.getElementById("net_worth").textContent = net_worth;
    document.getElementById("gain_loss").textContent = gain_loss;
    document.getElementById("price").textContent = price;
}

function gainLossIndicatorColor(){
    let gain_loss_value = document.getElementById("gain_loss").textContent;
    
    if (Number(gain_loss_value) >= 0){
        document.getElementById("gain_loss").style.color = "#00FD8F";
    }else{
        document.getElementById("gain_loss").style.color = "red";
    }
}

function main(){
    getAssets();
    getIndicators();
}

main()
