const table = document.querySelectorAll('.table');
const row = document.querySelectorAll('.row');

let draggedItem = null;

console.log(table);
console.log(row);

for (let i = 0; i < row.length; i++) {
    const item = row[i];

    item.addEventListener('dragstart', function() {
        draggedItem = item;
        setTimeout(function() {
            item.style.display = 'none';
        }, 0)
    });

    item.addEventListener('dragend', function() {
        setTimeout(function() {
            draggedItem.style.display = '';
            draggedItem = null;
        }, 0);
    })

    for (let j = 0; j < table.length; j++) {
        const list = table[j];

        list.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        list.addEventListener('dragenter', function(e) {
            e.preventDefault();
        });

        list.addEventListener('drop', function(e) {
            this.append(draggedItem);
        });
    }
}