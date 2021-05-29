function removeRoomForm() {
    document.getElementById('removeRoomForm').style.display = 'flex';
    document.getElementById('closeRemoveRoomForm').addEventListener('click',
        function() {
            document.getElementById('removeRoomForm').style.display = 'none';
        });

}


async function removeRoom() {
    var removeLink = "http://localhost:5000/api/dbService?function=delete_room&params=";
    var deleted = false;
    var problem = false;
    for (const i of document.getElementById('removeRoomsTable').children) {
        var selected = i.children[0].className;
        if (selected == "roomNicknameTdSelected") {
            deleted = true;
            var id = i.children[2].getElementsByTagName('tbody')[0].id;
            const f = fetch(removeLink + id.toString(), { method: 'POST', mode: "cors" }).then(
                    fetcheddata => fetcheddata.json())
                .then(data => {
                    if (parseInt(data['status']) == 0) {} else {
                        problem = true;
                    }
                })
            deleted = true;
            await f;
        }

    }
    if (problem) {
        alert("A problem occured when removing the room!");
        return;
    }
    if (deleted) {
        alert("Room/s deleted!");
        location.reload();
    } else {
        alert("No room selected!")
    }


}