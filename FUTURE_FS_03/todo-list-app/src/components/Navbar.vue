<template>
    <nav>
        <div v-if="username">
            Welcome, {{ username }}
        </div>
        <div v-else>
            <router-link to="/login">Login</router-link>
            <router-link to="/register">Register</router-link>
        </div>
    </nav>
</template>

<script>
export default{
    data(){
        return{
            username: localStorage.getItem('username'),
        };
    };
};
</script>