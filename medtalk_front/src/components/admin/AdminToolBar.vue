<template>
  <q-toolbar>
    <q-btn flat dense round icon="menu" aria-label="Menu" @click="emit('switch-left')">
      <q-tooltip> 隐藏 </q-tooltip>
    </q-btn>

    <q-toolbar-title style="max-width: 200px"> MedTalk Admin </q-toolbar-title>
    <q-breadcrumbs class="text-white" active-color="text-white" v-if="nav">
      <q-breadcrumbs-el icon="home" label="Home" />
      <q-breadcrumbs-el :icon="nav.first.icon" :label="nav.first.label" />
      <q-breadcrumbs-el icon="dashboard" :label="nav.second.label" />
    </q-breadcrumbs>
    <q-space />
    <q-btn flat round dense icon="reply" class="q-mr-xs" @click="toChat()"> <q-tooltip> 回到聊天 </q-tooltip></q-btn>
    <q-btn
      flat
      round
      dense
      class="q-mr-xs"
      :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
      @click="$q.fullscreen.toggle()"
    >
      <q-tooltip>
        {{ $q.fullscreen.isActive ? "窗口" : "全屏" }}
      </q-tooltip>
    </q-btn>

    <q-btn flat round dense>
      <!-- <q-badge color="red" rounded floating>4</q-badge> -->
      <q-avatar size="32px">
        <img :src="userStore.avatar" />
      </q-avatar>
      <q-menu>
        <q-list dense style="min-width: 100px">
          <q-item clickable v-close-popup>
            <q-item-section @click="showUserInfo()">个人信息</q-item-section>
          </q-item>
          <q-item clickable v-close-popup>
            <q-item-section @click="onLogout()">退出</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
      <q-tooltip> 用户 </q-tooltip>
    </q-btn>
    <q-btn flat round dense class="q-mr-xs" icon="o_settings" @click="emit('switch-right')">
      <q-tooltip> 个性化 </q-tooltip>
    </q-btn>
  </q-toolbar>
</template>

<script lang="ts" setup>
import { logout } from "@/api/login";
import { appMenu } from "@/store/app-store";
import { useUserStore } from "@/store/user";

const $router = useRouter();
const $route = useRoute();
const $q = useQuasar();
const menus = appMenu().menus;
const userStore = useUserStore();

const emit = defineEmits<{
  "switch-left": [];
  "switch-right": [];
}>();

const nav = computed(() => {
  for (const p of menus) {
    for (const q of p.children) {
      if (q.page === $route.name) {
        return { first: p, second: q };
      }
    }
  }
});

function toChat() {
  $router.push({ name: "chat" });
}

const showUserInfo = () => {
  $router.push({ name: "user-info" });
};

async function onLogout() {
  console.log("logout");
  await logout();
  userStore.logout();
  $router.push({ name: "login" });
}

onMounted(userStore.fetch);
</script>
