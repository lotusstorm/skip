<template>
    <div class="app_wrapper">
        <app-container>
            <div class="table">
                <div class="title">
                    <h1 class="content">Issues</h1>
                </div>
                <router-view/>
            </div>
        </app-container>
    </div>
</template>

<script>
    import Container from '@/components/Container.vue'

    export default {
        data() {
            return {
                showAddPanel: false,
            }
        },
        components: {
            'app-container': Container,
        },
    }
</script>
