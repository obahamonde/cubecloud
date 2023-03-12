<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
import MonacoEditor from "monaco-editor-vue3";
import { monacoOptions } from "../hooks/monaco";
import { usePython } from "usepython"
const { user } = useAuth0();

const py = usePython();

const codefile = reactive({
  name: "New File",
  content: "",
  last_modified: "",
});

const titleEditable = ref(false);


const meta = computed(() => {
  const ext = codefile.name.split(".").pop();
  switch(ext){
    case "js":
      return {
        icon: "mdi-language-javascript",
        language: "javascript",
        content_type: "text/javascript",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user.value.sub || "Anonymous",
      };
    case "ts":
      return {
        icon: "mdi-language-typescript",
        language: "typescript",
        content_type: "text/typescript",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
    case "html":
      return {
        icon: "mdi-language-html5",
        language: "html",
        content_type: "text/html",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
    case "css":
      return {
        icon: "mdi-language-css3",
        language: "css",
        content_type: "text/css",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
    case "json":
      return {
        icon: "mdi-code-braces",
        language: "json",
        content_type: "application/json",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
    case "md":
      return {
        icon: "mdi-language-markdown",
        language: "markdown",
        content_type: "text/markdown",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
    case "py":
      return {
        icon: "mdi-language-python",
        language: "python",
        content_type: "text/x-python",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
    default:
      return {
        icon: "mdi-file",
        content_type: "text/plain",
        size: codefile.content.length,
        last_modified: codefile.last_modified,
        owner: user?.value?.sub || "Anonymous",
      };
  }
});

const handleTitle = () => {
  if (titleEditable.value===false){ return;}
  titleEditable.value = true;
};

</script>

<template>
  <p text-white text-md text-center text-sm px-2 py-1
  :class="isDark ? 'bg-#1e1e1e text-white' : 'bg-#FFFFFE text-black'"
  @click="handleTitle()"
  class="w-48 sh"
  v-if="titleEditable"
  >
  {{ codefile.name }}
  </p>
  <p text-white text-md
  :class="isDark ? 'bg-#1e1e1e text-white' : 'bg-#FFFFFE text-black'"
  v-else
  >
  <input
  text-md
  text-center
  type="text"
  v-model="codefile.name"
  @keydown.enter="titleEditable = false"
  class="w-48 sh"
  placeholder="File Name"
  :class="isDark ? 'bg-#1e1e1e text-white' : 'bg-#FFFFFE text-black'"
  no-outline
  />
  </p>
  <MonacoEditor
        :theme="isDark ? 'vs-dark' : 'vs'"
        :options="monacoOptions"
        :language="meta.language"
        v-model:value="codefile.content"
        @change="codefile.last_modified = Date.now().toLocaleString()"        
      />
   
</template>