<template>
  <div class="login-page">
    <q-parallax :height="720">
      <!-- <template v-slot:media>
        <video width="720" height="440" poster="/login-video.mp4" autoplay loop muted>
          <source type="video/mp4" src="/img/login-video.mp4" />
        </video>
      </template> -->
      <div class="w-1/2 h-1/2">
        <q-card flat class="bg-white text-black">
          <div class="row">
            <div class="col-md-6 col-xs-12 q-pa-md" style="width: 50%; height: 50%">
              <q-img
                class="w-full h-full mx-auto object-cover"
                placeholder-src="/img/bot.jpg"
                src="/img/bot.jpg"
                spinner-color="white"
              />
            </div>
            <div class="col-md-6 col-xs-12">
              <router-view />
            </div>
          </div>
        </q-card>
      </div>
    </q-parallax>
  </div>
</template>
<script setup lang="ts"></script>

<style lang="scss">
.login-page {
  background-image: url("/img/bg.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  height: 100vh;
}
</style>
