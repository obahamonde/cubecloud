<script setup lang="ts">
//Importing dependencies
import { useAuth0 } from "@auth0/auth0-vue";
import { User } from "../hooks";
const { state, notify } = useStore();

//Using auth0
const {
  isAuthenticated,
  getAccessTokenSilently,
  user,
  logout,
  loginWithRedirect,
} = useAuth0();

//Getting user info from the API
const getUserInfo = async () => {
  if (state.user) return;
  const token = await getAccessTokenSilently();
  const { data } = await useFetch(`/api/auth?token=${token}`).json();
  state.user = unref(data) as User;
  const message = `Welcome ${state.user.name}!`;
  notify({
    message,
    status: "success",
  });
};

//Getting Completions from the API

//Pushing the message to the state

//Sending the message to the API

//OnMounted hook
onMounted(async () => {
  if (isAuthenticated.value) {
    await getUserInfo();
  } else {
    await loginWithRedirect();
  }
});
</script>
<template>
  <div
    class="row start items-center gap-4 px-4 py-2 text-white shadow-black shadow-lg backdrop-blur-md bottom-0 fixed w-full"
    bg-secondary
  >
    <img
      class="rf sh x4"
      :src="
        user.picture
          ? user.picture
          : 'https://media.istockphoto.com/id/1167753373/vector/woman-avatar-isolated-on-white-background-vector-illustration-for-your-design.jpg'
      "
    />

    <VBtn
      title="Logout"
      :class="
        isDark
          ? 'bg-red-500 ml-3 text-white scale cp'
          : 'bg-red-700 ml-3 text-white scale cp'
      "
      class="right-4 absolute"
      @click="logout()"
      icon
    >
      <VIcon>mdi-logout </VIcon>
    </VBtn>
  </div>
</template>
