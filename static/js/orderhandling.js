var itemList = new Object();
var shippingPrice = 5;
function makeChoice(whichbox) {
    with (whichbox.form) {
        if (whichbox.checked == false || whichbox.type.search("button") != -1) {
            delete itemList[whichbox.name]
        } else {
            itemList[whichbox.name] = new Array();
            if (whichbox.name == "Shipping") {
                itemList[whichbox.name][0] = 0;
            } else {
                itemList[whichbox.name][0] = whichbox.value;
            }
            if (whichbox.type.search("select") == -1) {
                itemList[whichbox.name][1] = whichbox.title;
            } else {
                numBooks = whichbox.options[whichbox.selectedIndex].title;
                if (numBooks*1 == 0) {
                    delete itemList[whichbox.name];
                    return formatCurrency(getPrice(whichbox));
                } else {
                    itemList[whichbox.name][1] = numBooks + "x" + whichbox.name;
               }
            }
            if (whichbox.name == "Patron" || whichbox.name == "Shipping") {
                itemList[whichbox.name][2] = 0;
            } else if (whichbox.type.search("select") != -1) {
                itemList[whichbox.name][2] = whichbox.options[whichbox.selectedIndex].title*1;
            } else if (whichbox.name == "Bundle") {
                itemList[whichbox.name][2] = 4;
            } else {
                itemList[whichbox.name][2] = 0;
            }
        }
        return formatCurrency(getPrice(whichbox));
    }
}
function getPrice(whichbox){
    totalPrice = 0;
    shipping = false;
    for (var i in itemList) {
        if (itemList[i][1] == "Shipping") {
            shipping = true;
        } else {
            totalPrice = parseInt(totalPrice) + parseInt(itemList[i][0]);
        }
    }
    if (shipping){
        for (var i in itemList) {
            if (itemList[i][1].search("Book") != -1 || i.search("Bundle") != -1) {
                totalPrice = parseInt(totalPrice) + parseInt(itemList[i][2]) * shippingPrice;
            }
        }
    }
    whichbox.form.amount.value = totalPrice;
    return totalPrice;
}
function concatNames(whichbox) {
    return(createString(itemList,whichbox));
}
function createString(itemArr,whichbox) {
    var orders=new Array();
    for (var i in itemArr) {
        orders.push(itemList[i][1]);
    }
    orders.sort();
    return(orders.toString());
}
function formatCurrency(num) {
    num = num.toString().replace(/\$|\,/g,'');
    if(isNaN(num))
        num = "0";
    cents = Math.floor((num*100+0.5)%100);
    num = Math.floor((num*100+0.5)/100).toString();
    if(cents < 10)
        cents = "0" + cents;
    for (var i = 0; i < Math.floor((num.length-(1+i))/3); i++)
        num = num.substring(0,num.length-(4*i+3))+','+num.substring(num.length-(4*i+3));
    return ("$" + num + "." + cents);
}
function clearPatronChoice(button) {
    for (i=0;i<button.form.Patron.length;i++) {
         button.form.Patron[i].checked = false;
     }
     delete itemList["Patron"]
}
function submitForm(s) {
    s.submitbutton.value = "Processing...";
    return true;
}

//Old books form
function processOrderString(){
    if(document.TransactionForm.shipping.checked){
        document.TransactionForm.merchantDefinedData4.value = document.TransactionForm.bookyear.value + "-Book, Shipping";
        document.getElementById("amountText").firstChild.nodeValue="65";
        document.TransactionForm.amount.value = "65";
    } else {
        document.TransactionForm.merchantDefinedData4.value = document.TransactionForm.bookyear.value + "-Book";
        document.getElementById("amountText").firstChild.nodeValue="60";
        document.TransactionForm.amount.value = "60";
    }
    document.TransactionForm.comments.value = document.TransactionForm.merchantDefinedData4.value	
}

