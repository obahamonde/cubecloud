<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { isAuthenticated, loginWithRedirect } = useAuth0();
</script>
<template>
  <div v-if="isAuthenticated">
    <VApp app>
      <RouterView />
    </VApp>
  </div>
  <div v-else class="landing">
    <AppLanding />
  </div>
</template>
<style global>
.landing {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url("/bg.gif");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-color: #36465d;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
