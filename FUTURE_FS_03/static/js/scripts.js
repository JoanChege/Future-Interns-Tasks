document.addEventListener("DOMContentLoaded", function () {
    const taskList = document.getElementById("task-list");

    // Example: Mark a task as complete
    taskList.addEventListener("click", function (event) {
        if (event.target.classList.contains("btn-success")) {
            const taskItem = event.target.closest("li");
            taskItem.classList.toggle("completed");
        }
    });

    // Example: Delete a task
    taskList.addEventListener("click", function (event) {
        if (event.target.classList.contains("btn-danger")) {
            const taskItem = event.target.closest("li");
            taskItem.remove();
        }
    });
});
