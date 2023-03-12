<script setup lang="ts">
const items = [
  {
    title: "Files",
    icon: "mdi-file-multiple-outline",
    to: "/",
  },
  {
    title: "Dashboard",
    icon: "mdi-view-dashboard",
    to: "/dashboard",
  },
  {
    title: "Settings",
    icon: "mdi-cog",
    to: "/settings",
  },
  {
    title: "About",
    icon: "mdi-information",
    to: "/about",
  },
];
</script>
<template>
<section
row start text-white  shadow-black shadow-lg backdrop-blur-md bg-secondary h-100vh
>
<nav col start p-2>
    <div
      v-for="item in items"
      
      class="col center"
    >
      <VBtn icon color="#36465D"
      :title="item.title"
      >
        <VIcon :icon="item.icon" text-white />
      </VBtn>
      </div>
    </nav>
<div>
  <AppTree/>
</div>
</section>
</template>