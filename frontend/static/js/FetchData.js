var dragging = false;
var serialNumber;

function addListener(obj) {
    obj.addEventListener('dragstart', () => {
        dragging = true;
        obj.classList.add('dragging');
    })
    obj.addEventListener('dragend', () => {
        dragging = false;
        setTimeout(function() { obj.classList.remove('dragging') }, 500);
    })
}

function addRoomsListenerDoubleClick(room) {
    room.addEventListener('dblclick', () => {
        fetch('http://localhost:5000/api/dbService?function=get_room_preferences&params=' + room.children[2].children[0].children[0].id, { method: 'GET', mode: "cors" }).then(
                fetcheddata => fetcheddata.json())
            .then(data => {
                var temperature = data['data'][0];
                var humidity = data['data'][1];
                var airQuality = data['data'][2];
                var economyFactor = data['data'][3];
                alert("Temperature: " + temperature + "\nHumidity: " + humidity + "\nAir Quality: " + airQuality + "\nEconomy factor: " + economyFactor);
            })
    });

}

function addTableListener(obj) {
    obj.addEventListener('dragover', () => {
        const draggable = document.querySelector('.dragging');
        serialNumber = draggable.getElementsByTagName('td')[2].innerHTML;
        obj.appendChild(draggable);
        outsideSensors.classList.add('currentList');
    })

    obj.addEventListener('dragleave', () => {
        outsideSensors.classList.remove('currentList');
    })

    obj.addEventListener('dragend', () => {
        console.log(obj.id);
        console.log(serialNumber);
        const f = fetch('http://localhost:5000/api/dbService?function=assign_sensor&params=' + obj.id + ',' + serialNumber + '', { method: 'POST', mode: "cors" }).then(
                fetcheddata => fetcheddata.json())
            .then(data => {
                alert(data['data']);
            })
    })
}

function alreadyExists(item, table) {
    var serial_number = null;
    var serial_number_item = item.getElementsByTagName('td')[2].innerHTML;
    for (var i = 0; i < table.length; i++) {
        serial_number = table[i].getElementsByTagName('td')[2].innerHTML;
        if (serial_number == serial_number_item) {
            return true;
        }
    }
}


function updateRowData(item, oldTable) {
    var value = item.getElementsByTagName('td')[4].innerHTML;
    var nickname = item.getElementsByTagName('td')[1].innerHTML;
    var serial_number = item.getElementsByTagName('td')[2].innerHTML;
    var old_serial_number;
    for (var i = 0; i < oldTable.length; i++) {
        old_serial_number = oldTable[i].getElementsByTagName('td')[2].innerHTML;
        if (old_serial_number == serial_number) {
            oldTable[i].getElementsByTagName('td')[4].innerHTML = value;
            oldTable[i].getElementsByTagName('td')[1].innerHTML = nickname;
            break;
        }
    }
}

function refresh(oldTableName, newTable) {
    var oldTable = oldTableName.getElementsByTagName('tr');
    var newItem = null;
    var oldItem = null;
    for (var i = 0; i < newTable.length; i++) {
        newItem = newTable[i];
        if (alreadyExists(newItem, oldTable)) {
            updateRowData(newItem, oldTable);
        } else {
            var row = oldTableName.insertRow();
            row.draggable = true;
            row.innerHTML = newItem.innerHTML;
            row.className = "draggable";
            addListener(row);
        }
    }
    for (var i = 0; i < oldTable.length; i++) {
        oldItem = oldTable[i];
        if (!alreadyExists(oldItem, newTable)) {
            oldTable[i].remove();
            return -1;
        }
    }
    return 0;
}

function refreshTable(tableName, tableData) {
    var oldTable = document.getElementById(tableName);
    var newTable = tableData.getElementsByTagName('tr');
    if (oldTable.getElementsByTagName('tr').length == 0) {
        oldTable.innerHTML = tableData.innerHTML;
        var rows = Array.prototype.slice.call(oldTable.getElementsByTagName('tr'));
        rows.forEach(element => {
            addListener(element);
        });
    }
    if (newTable.length == 0) {
        oldTable.innerHTML = "";
    } else {
        for (var i = 0; i < newTable.length; i++) {
            if (refresh(oldTable, newTable) == -1) {
                break;
            }
        }
    }
}

function get_room_devices(id, tbody_devices, array) {
    var result = [];
    var capability = undefined;
    var image = "svg/aerial-signal.svg";
    var row = null;
    var serial_number = null;
    var nickname = "";
    var curentValue = null;
    var description;
    for (var i = 0; i < array.length; i++) {
        if (array[i][0] == id) {
            description = "Sensor";
            capability = JSON.parse(array[i][4])["measure"];
            if (capability == undefined) {
                description = "Device";
                capability = JSON.parse(array[i][4])["action"];
                image = "svg/processor.svg";
            }
            nickname = array[i][2];
            curentValue = array[i][3];
            if (nickname == "") {
                nickname = "NONE";
            }
            if (curentValue == null) {
                curentValue = " ";
            }
            serial_number = array[i][1];
            row = tbody_devices.insertRow()
            row.draggable = true;
            row.classList.add("draggable");
            row.innerHTML = '\
                <td width=\'50px\'><object data=\'' + image + '\' width=\'35\' height=\'35\'>' + description + '</object></td > \
                <td>' + nickname + '</td> \
                <td>' + serial_number + '</td> \
                <td>' + capability + '</td> \
                <td>' + curentValue + '</td>';
        }
    }
    return result;
}

async function getUnassignedDevices() {
    var result = document.createElement('tbody');
    result.id = "UnassignedDevicesTable";

    var image;
    var serial_number;
    var nickname = "";
    var curentValue = null;
    var capability = undefined;
    var row = null;
    var description;
    await fetch('http://localhost:5000/api/dbService?function=get_unassigned_devices')
        .then(fetchedData => fetchedData.json())
        .then(data => {
            for (var i = 0; i < data['data'].length; i++) {
                description = 'Sensor';
                image = "svg/aerial-signal.svg";
                serial_number = data['data'][i][1];
                nickname = data['data'][i][2];
                curentValue = data['data'][i][3];
                capability = JSON.parse(data['data'][i][4])["measure"];
                if (capability == undefined) {
                    capability = JSON.parse(data['data'][i][4])["action"];
                    image = "svg/processor.svg";
                    description = 'Device'
                }
                if (nickname == "") {
                    nickname = "NONE";
                }
                if (curentValue == null) {
                    curentValue = " ";
                }
                row = result.insertRow();
                row.draggable = true;
                row.className = "draggable";

                row.innerHTML = "<td width='50px'><object data=\"" + image + "\" width='35' height='35'>" + description + "</object>\n" +
                    "<td>" + nickname + "</td><td>" + serial_number + "</td><td>" + capability + "</td><td>" + curentValue + "</td>";
            }
        });
    return result;
}

async function getOutsideSensors() {
    var result = document.createElement('tbody');
    result.className = "outsideDevicesTable";
    result.id = "OutsideDevicesTable";
    var serial_number;
    var nickname = "";
    var curentValue = null;
    var capability = undefined;
    await fetch('http://localhost:5000/api/dbService?function=get_outside_sensors')
        .then(fetchedData => fetchedData.json())
        .then(data => {
            for (var i = 0; i < data['data'].length; i++) {
                serial_number = data['data'][i][1];
                nickname = data['data'][i][2];
                curentValue = data['data'][i][3];
                capability = JSON.parse(data['data'][i][4])["measure"];
                if (nickname == "") {
                    nickname = "NONE";
                }
                if (curentValue == null) {
                    curentValue = " ";
                }
                row = result.insertRow();
                row.draggable = true;
                row.classList.add("draggable");
                row.innerHTML = "<td width='50px' class='draggable'><object data='svg/aerial-signal.svg' width='35' height='35'>" + "Sensor" + "</object>\n" +
                    "<td>" + nickname + "</td><td>" + serial_number + "</td><td>" + capability + "</td><td>" + curentValue + "</td>";
            }
        });
    return result;
}



async function get_rooms() {
    var result = document.createElement('tbody');
    var id = null;
    var nickname = "";
    var temperature = null;
    var humidity = null;
    var airQuality = null;
    var row = null;
    var allDevices = null;
    await fetch("http://localhost:5000/api/dbService?function=get_rooms")
        .then(fetchedData => fetchedData.json())
        .then(data => {
            for (var i = 0; i < data['data'][0].length; i++) {
                id = data['data'][0][i][0];
                nickname = data['data'][0][i][1];
                objectiveSpeed = data['data'][0][i][5];
                temperature = data['data'][0][i][6];
                humidity = data['data'][0][i][7];
                airQuality = data['data'][0][i][8];
                allDevices = data['data'][1];
                if (nickname == null) {
                    nickname = " ";
                }
                if (temperature == null) {
                    temperature = " ";
                }
                if (humidity == null) {
                    humidity = " ";
                }
                if (airQuality == null) {
                    airQuality = " ";
                }
                row = result.insertRow();
                var td_nickname = document.createElement('td');
                td_nickname.innerHTML = nickname;
                var td_information = document.createElement('td');
                td_information.innerHTML = 'Temp: ' + temperature + '??C<br>Humidity: ' + humidity + '%<br>Air Quality: ' + airQuality + ' of 10';
                var td_assigned_devices = document.createElement('td');
                td_nickname.className = "roomNicknameTd";
                td_information.className = "roomInformationTd";
                td_assigned_devices.className = "roomDevicesTd"
                row.append(td_nickname);
                row.append(td_information);
                row.append(td_assigned_devices);

                var table = document.createElement('table');
                table.className = 'roomDevicesParentTable';
                td_assigned_devices.append(table);
                td_assigned_devices.className = "roomDevicesTable";
                var tbody = document.createElement('tbody');
                tbody.id = id.toString();
                tbody.className = "devicesTable";
                table.append(tbody);

                get_room_devices(id, tbody, allDevices);
            }
        });
    return result;
}

function roomStillExists(oldTable, id) {
    var old_id = null;
    for (var i = 0; i < oldTable.length; i++) {
        old_id = oldTable[i].children[2].getElementsByTagName('tbody')[0].id
        if (id == old_id) {
            return true;
        }
    }
    return false;
}

function add_room(id, nickname, information, tableName) {
    var result = document.getElementById(tableName);
    row = result.insertRow();
    var td_nickname = document.createElement('td');
    td_nickname.className = "roomNicknameTd";
    td_nickname.innerHTML = nickname;
    var td_information = document.createElement('td');
    td_information.className = "roomInformationTd";
    td_information.innerHTML = information;
    var td_assigned_devices = document.createElement('td');
    td_assigned_devices.className = "roomDevicesTable";
    row.append(td_nickname);
    row.append(td_information);
    row.append(td_assigned_devices);

    var table = document.createElement('table');
    table.className = 'roomDevicesParentTable';
    td_assigned_devices.append(table);
    var tbody = document.createElement('tbody');
    tbody.id = id.toString();
    tbody.className = "devicesTable";
    addTableListener(tbody);
    table.append(tbody);
    addRoomsListenerDoubleClick(row);
}

function refreshRooms(tableName, newTable) {
    var oldTable = document.getElementById(tableName).children;
    var newTableArray = newTable.children;
    if (oldTable.length == 0) {
        if (newTable.innerHTML != "") {
            document.getElementById(tableName).innerHTML = newTable.innerHTML;
            var allTables = document.getElementsByClassName('devicesTable');
            if (tableName == 'roomsTable') {
                for (var i = 0; i < allTables.length; i++) {
                    addTableListener(allTables[i]);
                    addRoomsListenerDoubleClick(allTables[i].parentElement.parentElement.parentElement)
                    var devices = allTables[i].getElementsByTagName('tr');
                    for (var j = 0; j < devices.length; j++) {
                        addListener(devices[j]);
                    }
                }
            }
        }
        return;
    }

    var room_id = null;
    var houseDevices
    var rowData;
    for (var i = 0; i < newTableArray.length; i++) {
        room_id = newTableArray[i].children[2].getElementsByTagName('tbody')[0].id;
        houseDevices = newTableArray[i].children[2].getElementsByTagName('tbody')[0];
        if (roomStillExists(oldTable, room_id)) {
            rowData = document.getElementById(room_id).parentNode.parentNode.parentNode.children;
            rowData[0].innerHTML = newTableArray[i].children[0].innerHTML;
            rowData[1].innerHTML = newTableArray[i].children[1].innerHTML;
            refreshTable(room_id, houseDevices);
        } else {
            var tableData = newTableArray[i].children;
            var nickname = tableData[0].innerHTML;
            var information = tableData[1].innerHTML;
            add_room(room_id, nickname, information, tableName);
            refreshTable(room_id, houseDevices);

        }
    }
}



function selectDelete() {
    if (this.children[0].className == "roomNicknameTd") {
        this.children[0].className = "roomNicknameTdSelected";
        this.children[1].className = "roomInformationTdSelected";
        this.children[2].className = "roomDevicesTdSelected";
    } else {
        this.children[0].className = "roomNicknameTd";
        this.children[1].className = "roomInformationTd";
        this.children[2].className = "roomDevicesTd";
    }
}

function selectPreferences() {

    for (const i of this.parentElement.children) {
        i.children[0].className = "roomNicknameTd";
        i.children[1].className = "roomInformationTd";
        i.children[2].className = "roomDevicesTd";
    }
    if (this.children[0].className == "roomNicknameTd") {
        this.children[0].className = "roomNicknameTdSelected";
        this.children[1].className = "roomInformationTdSelected";
        this.children[2].className = "roomDevicesTdSelected";
    } else {
        this.children[0].className = "roomNicknameTd";
        this.children[1].className = "roomInformationTd";
        this.children[2].className = "roomDevicesTd";
    }
}

async function updateFields() {
    if (!dragging) {
        refreshTable('UnassignedDevicesTable', await getUnassignedDevices());
        refreshTable('OutsideDevicesTable', await getOutsideSensors());
        var rooms = await get_rooms();
        refreshRooms('roomsTable', rooms);
        refreshRooms('removeRoomsTable', rooms);
        refreshRooms('preferencesRoomsTable', rooms);


        for (const i of document.getElementById('removeRoomsTable').children) {
            i.onclick = selectDelete;
        }
        for (const i of document.getElementById('preferencesRoomsTable').children) {
            i.onclick = selectPreferences;
        }
    }
    setTimeout(updateFields, 5000);
}



updateFields();