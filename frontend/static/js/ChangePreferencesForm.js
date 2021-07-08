var selectedId;

function preferencesRoomForm() {
    document.getElementById('preferencesRoomForm').style.display = 'flex';
    document.getElementById('closePreferencesRoomForm').addEventListener('click',
        function() {
            document.getElementById('preferencesRoomForm').style.display = 'none';
        });
    document.getElementById('closeSettingsRoomForm').addEventListener('click',
        function() {
            document.getElementById('roomSettingsForm').style.display = 'none';
        });
}

function roomSettingsForm(nickname, temperature, humidity, airQuality, objectiveSpeed) {
    document.getElementById('roomSettingsForm').style.display = 'flex';
    document.getElementById('settingsNickname').value = nickname;
    document.getElementById('settingsTemperature').value = temperature;
    document.getElementById('settingsHumidity').value = humidity;
    document.getElementById('settingsAirQuality').value = airQuality;
    document.getElementById('settingsObjectiveSpeed').value = objectiveSpeed;
    document.getElementById('closeSettingsRoomForm').addEventListener('click',
        function() {
            document.getElementById('roomSettingsForm').style.display = 'none';
        });
}

async function commitChanges() {
    var id = selectedId;
    var nickname = document.getElementById('settingsNickname').value;
    var temperature = document.getElementById('settingsTemperature').value;
    var humidity = document.getElementById('settingsHumidity').value;
    var airQuality = document.getElementById('settingsAirQuality').value;
    var economyFactor = document.getElementById('settingsObjectiveSpeed').value;
    const f = fetch("http://localhost:5000/api/dbService?function=update_room&params=" + id.toString() + "," + nickname + "," + temperature.toString() + "," + humidity.toString() + "," + airQuality.toString() + "," + economyFactor.toString(), { method: 'POST', mode: "cors" }).then(
        fetcheddata => fetcheddata.json()).then(
        data => {
            if (parseInt(data['status']) == 0) {
                alert("Room settings changed succesfully!");
                location.reload();
            } else {
                alert("A problem occured when changing room settings!");
            }

        }
    )
    await f;
}


async function changeRoomPreferences() {
    var getRoomPreferences = "http://localhost:5000/api/dbService?function=get_room_preferences&params=";
    var problem = false;
    var selected = false;
    for (const i of document.getElementById('preferencesRoomsTable').children) {
        var selected = i.children[0].className;
        if (selected == "roomNicknameTdSelected") {
            var id = i.children[2].getElementsByTagName('tbody')[0].id;
            const f = fetch(getRoomPreferences + id.toString(), { method: 'GET', mode: "cors" }).then(
                    fetcheddata => fetcheddata.json())
                .then(data => {
                    if (parseInt(data['status']) == 0) {
                        roomSettingsForm(data['data'][4], data['data'][0], data['data'][1], data['data'][2], data['data'][3]);
                        selectedId = id;
                        selected = true;
                    } else {
                        problem = true;
                    }
                })
            await f;
            break;
        }

    }
    if (problem) {
        alert("A problem occured when changing room preferences!");
        return;
    }
    if (!selected) {
        alert("No room selected!")
    }
}