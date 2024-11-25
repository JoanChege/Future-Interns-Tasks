const form = document.getElementById('todo-form');
const taskList = document.getElementById('task-list');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const taskName = document.getElementById('task-name').value;
    const taskDate = document.getElementById('task-date').value;
    const taskNotes = document.getElementById('task-notes').value;

    if (!taskName || !taskDate) {
        alert('Task name and due date are required!');
        return;
    }

    const listItem = document.createElement('li');
    listItem.className = 'list-group-item d-flex justify-content-between align-items-start';

    listItem.innerHTML = `
        <div>
            <strong>${taskName}</strong> <br>
            <small>Due: ${taskDate}</small><br>
            <small>${taskNotes}</small>
        </div>
        <div>
            <button class="btn btn-success btn-sm complete-btn">✔</button>
            <button class="btn btn-danger btn-sm delete-btn">✖</button>
        </div>
    `;

    taskList.appendChild(listItem);

    // Clear form inputs
    document.getElementById('task-name').value = '';
    document.getElementById('task-date').value = '';
    document.getElementById('task-notes').value = '';
});

taskList.addEventListener('click', (e) => {
    if (e.target.classList.contains('complete-btn')) {
        e.target.parentElement.parentElement.querySelector('strong').classList.toggle('completed');
    }
    if (e.target.classList.contains('delete-btn')) {
        e.target.parentElement.parentElement.remove();
    }
});
