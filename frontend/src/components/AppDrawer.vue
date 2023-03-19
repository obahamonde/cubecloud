<script setup lang="ts">
const items = ref([
  {
    title: "Files",
    icon: "mdi-file-multiple-outline",
  },
  {
    title: "Dashboard",
    icon: "mdi-view-dashboard",
  },
  {
    title: "Settings",
    icon: "mdi-cog",
  },
  {
    title: "About",
    icon: "mdi-information",
  },
]);

const currentRoute = ref("Files");

const push = (route: string) => {
  currentRoute.value = route;
};
</script>
<template>
  <section row start text-white shadow-black shadow-lg backdrop-blur-md bg-secondary h-100vh>
    <nav col start p-2>
      <div v-for="item in items" class="col center">
        <VBtn icon color="#36465D" :title="item.title" @click="push(item.title)">
          <VIcon :icon="item.icon" text-white />
        </VBtn>
      </div>
    </nav>
    <div>
      <div v-if="currentRoute === 'Files'">
        <AppTree />
      </div>
      <div v-if="currentRoute === 'Dashboard'">
        <AppDashBoard />
      </div>
      <div v-if="currentRoute === 'Settings'">
        <AppSettings />
      </div>
      <div v-if="currentRoute === 'About'">
        <AppAbout />
      </div>
    </div>
  </section>
</template>
