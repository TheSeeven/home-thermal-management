var serialNumber = "";

const unasignedDevicesTable = document.getElementById('UnassignedDevicesTable');
const outsideSensors = document.getElementById('OutsideDevicesTable');



unasignedDevicesTable.addEventListener('dragover', () => {
    const draggable = document.querySelector('.dragging');
    serialNumber = draggable.getElementsByTagName('td')[2].innerHTML;
    unasignedDevicesTable.appendChild(draggable);
    outsideSensors.classList.add('currentList');
})

unasignedDevicesTable.addEventListener('dragleave', () => {
    outsideSensors.classList.remove('currentList');
})

unasignedDevicesTable.addEventListener('dragend', () => {
    if (serialNumber == "") {
        return;
    }
    const f = fetch('http://localhost:5000/api/dbService?function=assign_sensor&params=' + 'NULL' + ',' + serialNumber + '', { method: 'POST', mode: "cors" }).then(
            fetcheddata => fetcheddata.json())
        .then(data => {
            alert(data['data']);
        })
})

outsideSensors.addEventListener('dragover', () => {
    const draggable = document.querySelector('.dragging');
    if (draggable.getElementsByTagName('td')[2].innerHTML.includes("processor")) {
        return;
    }
    serialNumber = draggable.getElementsByTagName('td')[2].innerHTML;
    outsideSensors.appendChild(draggable);
    outsideSensors.classList.add('currentList');
})

outsideSensors.addEventListener('dragleave', () => {
    outsideSensors.classList.remove('currentList');
})

outsideSensors.addEventListener('dragend', () => {
    const draggable = document.querySelector('.dragging');
    if (draggable.getElementsByTagName('td')[0].innerHTML.includes("processor")) {
        return;
    }
    const f = fetch('http://localhost:5000/api/dbService?function=assign_sensor&params=' + '-1' + ',' + serialNumber + '', { method: 'POST', mode: "cors" }).then(
            fetcheddata => fetcheddata.json())
        .then(data => {
            alert(data['data']);
        })
})