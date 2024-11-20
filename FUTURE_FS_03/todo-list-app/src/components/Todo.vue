<template>
    <div>
        <input v-model="newTask" placeholder="Add a new task" @keyup.enter="addTask">
        <ul>
            <li v-for="(task, index) in tasks" :key="task.id">
                <span :class="{ completed: task.completed }"{{ task.text }}></span>
                <button @click="deleteTask(index)">Delete Task</button>
                <button @click="markComplete(index)">Mark Complete</button>
            </li>
        </ul>
    </div>
</template>

<script>
export default{
    data(){
        return{
            newTask: '',
            tasks: [],
        };
    },
    methods: {
        addTask(){
            const task = { text: this.newTask, completed: false};
            this.tasks.push(task);
            this.newTask = '';
        },
        deleteTask(index){
            this.tasks.splice(index, 1);
        },
        markComplete(index){
            this.tasks[index].completed = !this.tasks[index].completed;
        }
    },
};
</script>

<style scoped>
    .completed {
        text-decoration: line-through;
    }
</style>