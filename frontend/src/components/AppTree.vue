import { Icon } from '@iconify/vue';
<script setup lang="ts">
const treeView = ref();
const repo = ref();
const owner = ref();

const { state } = useStore();

const getTree = async () => {
  const response = await fetch(`/api/repos/${owner.value}/${repo.value}`);
  const data = await response.json();
  treeView.value = data.children[0].children;
};

const getIcon = (name: string) => {
  if (name === "Dockerfile") return "logos:docker-icon";
  const ext = name.split(".").pop();
  switch (ext) {
    case "py":
      return "logos:python";
    case "js":
      return "logos:javascript";
    case "html":
      return "logos:html-5";
    case "css":
      return "logos:css-3";
    case "json":
      return "logos:json";
    case "md":
      return "logos:markdown";
    case "txt":
      return "bxs:file-txt";
    case "yml":
      return "logos:yaml";
    case "xml":
      return "logos:yaml";
    case "svg":
      return "logos:svg";
    case "png":
      return "bxs:file-png";
    default:
      return "bxs:file";
  }
};

onMounted(async () => {
  if (!owner.value || !repo.value) {
    return;
  }
  await getTree();
});

const tab = ref(false);

const visible = ref(false);

const topVisible = ref(false);

onUnmounted(() => {
  Object.assign(state.codeSpace, {
    treeView: treeView.value,
    owner: owner.value,
    repo: repo.value,
    currentFile: null,
  });
});
</script>

<template>
  <div>
    <div col start h-screen w-48 p-4 bg-secondary sh>
      <Icon
        :icon="topVisible ? 'mdi-chevron-double-up' : 'mdi-chevron-double-down'"
        class="scale cp"
        @click="topVisible = !topVisible"
      />
      <div v-if="topVisible">
        <div v-if="!visible">
          <div row center>
            <Icon
              x3
              rf
              scale
              sh
              cp
              mx-2
              top-4
              p-1
              invert
              icon="logos:github-icon"
              :class="tab ? '' : 'bg-white'"
              @click="tab = false"
            />
            <Icon
              x3
              rf
              scale
              sh
              cp
              mx-2
              top-4
              p-1
              text-white
              icon="mdi-cloud-upload"
              :class="tab ? 'bg-black' : ''"
              @click="tab = true"
            />
          </div>
          <div
            my-4
            p-2
            w-40
            bg-transparent
            text-white
            font-extrabold
            v-if="!tab"
          >
            <VTextField v-model="owner" label="Owner" placeholder="Owner  " />
            <VTextField
              v-model="repo"
              label="Repo"
              placeholder="Repo"
              @keyup.enter="getTree()"
            />
          </div>
          <div v-else col center>
            <AppUpload />
          </div>
        </div>
      </div>
      <ul col start>
        <li
          v-for="item in treeView"
          class="col w-full start cp scale decoration-none list-none text-white text-md font-bold hover:bg-primary hover:bg-opacity-50 rounded-md"
          @click="state.currentFile = item"
        >
          <div row center>
            <Icon
              :icon="getIcon(item.name)"
              v-if="item.type === 'file'"
              class="mx-2"
            />
            {{ item.name }}
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
