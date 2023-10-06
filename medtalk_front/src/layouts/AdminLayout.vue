<template>
  <q-layout view="hHh LpR fFf">
    <q-header class="shadow-1">
      <admin-tool-bar @switch-right="toggleRightDrawer" @switch-left="toggleLeftDrawer" />
    </q-header>

    <q-drawer
      class="shadow-0"
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :width="200"
      id="left-menu"
    >
      <admin-left-menu />
    </q-drawer>

    <q-drawer
      class="l-shadow-3"
      no-swipe-backdrop
      v-model="rightDrawerOpen"
      side="right"
      bordered
      overlay
      :width="240"
      @mouseleave="toggleRightDrawer"
    >
      <u-i-config />
    </q-drawer>
    <q-page-container class="main-container">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
const leftDrawerOpen = ref(false);
const rightDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function toggleRightDrawer() {
  rightDrawerOpen.value = !rightDrawerOpen.value;
}
</script>
