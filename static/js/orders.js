function addBook(divName){
    var newdiv = document.createElement('div');
    newdiv.innerHTML = "Entry"
    document.getElementById(divName).appendChild(newdiv);
}
