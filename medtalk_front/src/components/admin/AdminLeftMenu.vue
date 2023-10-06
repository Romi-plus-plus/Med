<template>
  <q-list>
    <q-expansion-item
      v-for="(module, index) in menus"
      :key="module.label"
      expand-separator
      :icon="module.icon"
      :label="module.label"
      :default-opened="true"
      header-class="left-menu-root"
    >
      <q-list>
        <template v-for="page in module.children" :key="page.page">
          <q-item
            v-if="userStore.hasPerm(page.perm)"
            class="left-menu-item"
            clickable
            v-ripple
            :to="{ name: page.page }"
          >
            <q-item-section avatar>
              <q-icon :name="page.icon" />
            </q-item-section>
            <q-item-section>{{ page.label }}</q-item-section>
          </q-item>
        </template>
      </q-list>
    </q-expansion-item>
  </q-list>
</template>

<script lang="ts" setup>
import { appMenu } from "@/store/app-store";
import { useUserStore } from "@/store/user";

const menus = appMenu().menus;
const userStore = useUserStore();
</script>
