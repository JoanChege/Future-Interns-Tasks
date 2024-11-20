new Vue({
    el: "#todo-app",
    data: {
        loggedIn: false,
        isRegistering: false,
        user: null,
        loginCredentials: { username: "", password: "" },
        newUser: { email: "", username: "", password: "" },
        newTask: "",
        tasks: []
    },
    methods: {
        toggleForm() {
            this.isRegistering = !this.isRegistering;
        },
        register() {
            const { email, username, password } = this.newUser;

            // Password Validation
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})/;
            if (!passwordRegex.test(password)) {
                alert("Password must have at least 8 characters, include uppercase, lowercase, and a special character.");
                return;
            }

            // Save user to "database"
            localStorage.setItem(username, JSON.stringify({ email, username, password, tasks: [] }));
            alert("Registration successful! Please login.");
            this.isRegistering = false;
        },
        login() {
            const { username, password } = this.loginCredentials;
            const userData = localStorage.getItem(username);

            if (!userData) {
                alert("User not found. Please register.");
                return;
            }

            const user = JSON.parse(userData);
            if (user.password !== password) {
                alert("Invalid password.");
                return;
            }

            this.loggedIn = true;
            this.user = user;
            this.tasks = user.tasks;
        },
        logout() {
            this.loggedIn = false;
            this.user = null;
            this.tasks = [];
            this.loginCredentials = { username: "", password: "" };
        },
        addTask() {
            if (!this.newTask.trim()) return;

            this.tasks.push({ name: this.newTask, completed: false });
            this.newTask = "";
            this.saveTasks();
        },
        deleteTask(index) {
            this.tasks.splice(index, 1);
            this.saveTasks();
        },
        saveTasks() {
            if (this.user) {
                const user = { ...this.user, tasks: this.tasks };
                localStorage.setItem(this.user.username, JSON.stringify(user));
            }
        }
    }
});
