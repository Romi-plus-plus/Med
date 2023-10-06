import { defineStore } from "pinia";

export const appMenu = defineStore("menus", () => {
  type Menu = {
    icon: string;
    label: string;
    children: { label: string; page: string; icon: string; perm?: string }[];
  };
  const menus = ref<Menu[]>([
    {
      icon: "addchart",
      label: "数据统计",
      children: [{ label: "业务总览", page: "index", icon: "dashboard" }],
    },
    {
      icon: "forum",
      label: "聊天管理",
      children: [
        { label: "会话管理", page: "admin-chat", icon: "chat", perm: "Chat management" },
        { label: "对话管理", page: "admin-message", icon: "chat_bubble", perm: "Chat management" },
        { label: "分享管理", page: "admin-share", icon: "share", perm: "Chat management" },
      ],
    },
    {
      icon: "business",
      label: "运营管理",
      children: [
        { label: "问答管理", page: "admin-question", icon: "cloud", perm: "Operation management" },
        { label: "推荐管理", page: "admin-recommend", icon: "recommend", perm: "Operation management" },
        { label: "投诉管理", page: "admin-complaint", icon: "feedback", perm: "Operation management" },
      ],
    },
    {
      icon: "settings",
      label: "系统管理",
      children: [
        { label: "用户管理", page: "admin-user", icon: "person", perm: "User management" },
        { label: "知识库", page: "admin-kg", icon: "bubble_chart", perm: "KB management" },
      ],
    },
  ]);

  return { menus };
});
