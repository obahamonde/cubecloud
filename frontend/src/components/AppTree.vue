<script setup lang="ts">
const treeView = reactive({
  data: [
    {
      id: 1,
      name: "Root node",
      children: [
        {
          id: 2,
          name: "Child node 1",
          children: [
            {
              id: 3,
              name: "Child node 1.1",
              children: [
                {
                  id: 4,
                  name: "Child node 1.1.1",
                  children: [
                    {
                      id: 5,
                      name: "Child node",
                        children: [],
                    }
                ],
                },
                ],
            },
            ]
            },
        ]
}]
})
</script>

<template>
<div col center h-screen w-36 p-2 bg-secondary sh >
  <div class="w-full h-full overflow-y-auto">
    <div v-for="item in treeView.data" :key="item.id" class="w-full">
          {{ item }}
    </div>
  </div>
</div>
</template>