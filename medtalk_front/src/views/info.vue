<template>
  <div class="row q-col-gutter-sm p-4 bg-primary-1">
    <div class="col-lg-8 col-md-8 col-xs-12 col-sm-12">
      <q-card class="bg-primary-2 no-shadow" bordered v-if="user">
        <q-banner rounded class="text-center bg-primary-3">
          <span class="text-h5"> 更新您的信息</span>
        </q-banner>

        <q-card-section class="q-pa-sm">
          <q-list class="row">
            <q-item class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
              <q-item-section side>
                <q-btn round @click="uploadState = !uploadState" title="点击上传新头像">
                  <q-avatar size="100px" class="shadow-2">
                    <img :src="userStore.avatar" />
                  </q-avatar>
                </q-btn>
              </q-item-section>
              <q-item-section>
                <q-uploader
                  v-if="uploadState"
                  style="max-width: 240px; max-height: 200px"
                  label="新头像"
                  accept=".jpg, image/*"
                  :factory="uploadAvatar"
                />
              </q-item-section>
            </q-item>

            <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
              <q-item-section>
                <q-input filled stack dense v-model="user.username" label="您的用户名" readonly />
              </q-item-section>
            </q-item>
            <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
              <q-item-section>
                <q-input filled stack dense v-model="user.email" label="您的邮箱" />
              </q-item-section>
            </q-item>
            <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
              <q-item-section>
                <q-input filled stack dense v-model="user.phone" label="您的号码" />
              </q-item-section>
            </q-item>
            <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
              <q-item-section>
                <q-input filled stack dense v-model="user.name" label="您的昵称" />
              </q-item-section>
            </q-item>
            <q-item class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
              <q-item-section> 当前密码 </q-item-section>
            </q-item>
            <q-item class="col-lg-8 col-md-8 col-sm-12 col-xs-12">
              <q-item-section>
                <q-input
                  type="password"
                  dense
                  filled
                  stack
                  v-model="password_dict.current_password"
                  label="当前密码"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn color="primary" @click="update">更新您的信息</q-btn>
        </q-card-actions>
      </q-card>

      <q-card class="bg-primary-2 no-shadow" bordered>
        <q-card-section class="text-h6 q-pa-sm">
          <div class="text-h6">更改密码</div>
        </q-card-section>
        <q-card-section class="q-pa-sm row">
          <q-item class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
            <q-item-section> 新密码 </q-item-section>
          </q-item>
          <q-item class="col-lg-8 col-md-8 col-sm-12 col-xs-12">
            <q-item-section>
              <q-input
                type="password"
                dense
                filled
                color="blue"
                stack
                v-model="password_dict.new_password"
                label="新密码"
              />
            </q-item-section>
          </q-item>
          <q-item class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
            <q-item-section> 确认新密码 </q-item-section>
          </q-item>
          <q-item class="col-lg-8 col-md-8 col-sm-12 col-xs-12">
            <q-item-section>
              <q-input
                type="password"
                filled
                dense
                stack
                v-model="password_dict.confirm_new_password"
                label="确认新密码"
              />
            </q-item-section>
          </q-item>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn color="primary" @click="updatePassword">更改密码</q-btn>
        </q-card-actions>
      </q-card>
    </div>
    <div class="col-lg-4 col-md-4 col-xs-12 col-sm-12">
      <q-card class="bg-primary-2 no-shadow" bordered>
        <q-card-section class="text-center bg-transparent">
          <q-avatar size="100px" class="shadow-10">
            <img
              src="https://img.freepik.com/free-vector/hospital-logo-design-vector-medical-cross_53876-136743.jpg?w=740&t=st=1693359039~exp=1693359639~hmac=e1c4b87396670f03b3fad1745015b3048e9f7224a5785073d789e63ae23c82be"
            />
          </q-avatar>
          <div class="text-subtitle2 q-mt-lg">by MedChat</div>
          <div class="text-h6 q-mt-md">MedChat</div>
        </q-card-section>
        <q-card-section>
          <div class="text-body2 text-justify">
            作为耳动辅助装置的配套问答系统，我是您的人工助手Med，代表我的核心技术是“Movement Ear Detection”,也和它的医疗属性暗合。我旨在为您提供准确、可靠的设备信息和答案，帮助您解答各种设备安全、安装使用、维修换新的问题和疑虑。无论是关于是硬件还是软件，我都可以为您提供专业建议和指导。实在遇到难以解决的问题，可以以问题投诉或者撰写反馈的方式告知我们，我们会第一时间联系客服小姐姐告诉你的。
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
  <!-- </q-page> -->
</template>

<script setup lang="ts">
import { User, updateUserMe, updateUserMeAvatar } from "@/api/user";
import { useUserStore } from "@/store/user";
import Message from "@/utils/message";

const userStore = useUserStore();

const user = ref<User>();
const password_dict = reactive({
  current_password: "",
  new_password: "",
  confirm_new_password: "",
});

const uploadState = ref(false);

onMounted(async () => {
  user.value = await userStore.fetch();
});

async function update(user_details: any) {
  try {
    Message.info("提交更新信息");
    user_details.value = await updateUserMe({
      email: user_details.email,
      phone: user_details.phone,
      name: user_details.name,
      password: "root",
      password2: "root",
    });
    Message.success(`更新成功！`);
  } catch (e) {
    console.log("update error");
  }
}
async function updatePassword(user_details: any) {
  try {
    Message.info("提交更新信息");
    user_details.value = await updateUserMe({
      email: user_details.email,
      phone: user_details.phone,
      name: user_details.name,
      password: "root",
      password2: "root",
    });
    Message.success(`更新成功！`);
  } catch (e) {
    console.log("update error");
  }
}

async function uploadAvatar(files: readonly File[]) {
  const file = files[0];
  if (file) {
    user.value = await updateUserMeAvatar(file);
    Message.success("成功更新头像！");
    uploadState.value = false;
  } else {
    Message.warning("你没有选择文件！");
  }
  return { url: "" };
}
</script>

<style scoped></style>
