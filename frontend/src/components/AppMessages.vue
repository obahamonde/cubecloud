<script setup lang="ts">
import { isDark } from "../hooks/dark";

import { useAuth0 } from "@auth0/auth0-vue";
import { useSynthesis } from "../hooks";

const { state } = useStore();

const { user } = useAuth0();

const { text, play } = useSynthesis();

const synthetize = (msg: Message) => {
  text.value = msg.message;
  msg.message = "";
  for (let i = 0; i < text.value.length; i++) {
    setTimeout(() => {
      msg.message += text.value[i];
    }, 50 * i);
  }
  play();
};

</script>
<template>
  <VContainer class="col gap-4">
    <VCard
      v-for="msg in state.messages"
      :class="msg.sender === 'user' ? 'col start' : 'col end'"
      pa-4
    >
      <div row center gap-2 mx-2>
        <div col center gap-1 v-if="msg.sender === 'user'">
          <img :src="user.picture" class="rf cp x2 sh" />
          <p
            :class="
              isDark
                ? 'text-caption text-primary'
                : 'text-caption text-teal-800'
            "
            v-text="msg.created_at"
          />
        </div>
        <VCardText v-text="msg.message" />
        <div v-if="msg.sender === 'bot'" col center gap-1>
          <img src="/logo.svg" class="rf cp x2 sh"
            @click="synthetize(msg)"
          />
          <p
            :class="
              isDark
                ? 'text-caption text-primary'
                : 'text-caption text-teal-800'
            "
            v-text="msg.created_at"
          />
        </div>
      </div>
    </VCard>
  </VContainer>
</template>
