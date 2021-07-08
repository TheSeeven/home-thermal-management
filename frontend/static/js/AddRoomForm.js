function addRoomForm() {
    document.getElementById('addRoomForm').style.display = 'flex';
    document.getElementById('closeAddRoomForm').addEventListener('click',
        function() {
            document.getElementById('addRoomForm').style.display = 'none';
            document.getElementById('nickname').value = "";
            document.getElementById('temperature').value = "";
            document.getElementById('humidity').value = "";
            document.getElementById('airQuality').value = "";
            document.getElementById('objectiveSpeed').value = "";
        });
}

async function addRoom() {
    let nickname = document.getElementById('nickname').value;
    let temperature = document.getElementById('temperature').value;
    let humidity = document.getElementById('humidity').value;
    let airQuality = document.getElementById('airQuality').value;
    let objectiveSpeed = document.getElementById('objectiveSpeed').value;
    fetch('http://localhost:5000/api/dbService?function=insert_room&params=' + nickname + ',' + temperature + ',' + humidity + ',' + airQuality + ',' + objectiveSpeed + '', { method: 'POST', mode: "cors" }).then(
            fetcheddata => fetcheddata.json())
        .then(data => {
            alert(data['data']);
            if (parseInt(data['status']) == 0) {
                document.getElementById('nickname').value = "";
                document.getElementById('temperature').value = "";
                document.getElementById('humidity').value = "";
                document.getElementById('airQuality').value = "";
                document.getElementById('objectiveSpeed').value = "";
            }
        })
}




temperature.oninput = function() {
    if (parseInt(this.value) > 50 || parseInt(this.value) < 1 || isNaN(parseInt(this.value))) {
        this.value = "";
        return;
    }
}


humidity.oninput = function() {
    if (parseInt(this.value) > 99 || parseInt(this.value) < 1 || isNaN(parseInt(this.value))) {
        this.value = "";
        return;
    }
}
airQuality.oninput = function() {
    if (parseInt(this.value) > 10 || parseInt(this.value) < 1 || isNaN(parseInt(this.value))) {
        this.value = "";
        return;
    }
}
objectiveSpeed.oninput = function() {
    if (parseInt(this.value) > 10 || parseInt(this.value) < 1 || isNaN(parseInt(this.value))) {
        this.value = "";
        return;
    }
}