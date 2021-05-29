function B_GET() {
    var xhttp = new XMLHttpRequest();
    var input = document.getElementById("input").value;

    xhttp.open("GET", "http://127.0.0.1:5000/" + input, false);
    xhttp.send();

    document.getElementById('output').innerHTML = xhttp.responseText;
    console.log(xhttp.responseText);
}

function B_POST() {

    var xhttp = new XMLHttpRequest();
    var input = document.getElementById("input").value;

    xhttp.open("POST", "localhost:5000/api/dbService?" + input, false);
    xhttp.send();
    console.log(input);
    document.getElementById('output').innerHTML = xhttp.responseText;
    console.log(xhttp.responseText);
}