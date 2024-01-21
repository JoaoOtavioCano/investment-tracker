import { getTransactions } from './transactions.js';

export function gotToTheEndOfTheScroll(){
    const table = document.getElementById("transactions-table-grid");

    table.addEventListener("scroll", () => {

        if (table.scrollTop + table.clientHeight >= table.scrollHeight) {
            console.log("scroll");
            getTransactions();
        }
    });
}