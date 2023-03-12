<template>
        <VBtn icon class="btn-circle right-4 absolute" @click="toggleDark()"
        dark:bg-secondary dark:text-white bg-white text-secondary
        >
      <VIcon
      :class="isDark ? 'text-amber' : 'text-cyan'"
      >
        {{ isDark ? "mdi-white-balance-sunny" : "mdi-weather-night" }}
      </VIcon>
    </VBtn>
</template>