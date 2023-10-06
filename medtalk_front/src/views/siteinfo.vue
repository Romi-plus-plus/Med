<template>
  <div class="about-section bg-primary-2">
    <div>
      <h1 class="text-h3" style="text-align: center; color: black">关于我们</h1>
    </div>
    <br />
    <div>
      <h3 class="text-h6" style="text-align: center; color: black">
        我们的使命是通过人工智能技术，为用户提供高质量的交互设备支持服务。我们希望通过这个系统，帮助用户解答设备的疑问，更好享受设备带来的便利。
      </h3>
    </div>
    <q-separator></q-separator>
    <div>
      <h3 class="text-h5" style="text-align: center; color: black">联系我们</h3>
    </div>
    <div>
      <h3 class="text-h7" style="text-align: center; color: black">
        如果你对我们的问答系统有任何疑问、建议或合作意向，欢迎与我们联系。你可以通过以下方式与我们取得联系：
      </h3>

      <h3 class="text-h7" style="text-align: center; color: black">
        <div>电子邮件：collinchen140@qq.com <br />电话：18195013957</div>
      </h3>
    </div>
  </div>
  <div class="text-container bg-primary-2">
    <h2 style="text-align: center; color: black">Our Team</h2>
  </div>
  <div class="row bg-primary-2">
    <div class="column">
      <div class="card">
        <img src="/img/kaa.jpg" alt="Kaa" style="width: 100%" />
        <div class="container">
          <h2>汤耀辉</h2>
          <p class="title">弱小无助的开发者</p>
          <p>kaadttc@gmail.com</p>
        </div>
      </div>
    </div>

    <div class="column">
      <div class="card">
        <img src="/img/chen.jpg" alt="Mike" style="width: 100%" />
        <div class="container">
          <h2>陈旭辉</h2>
          <p class="title">满腔热血的废物</p>
          <p>Raschel.Chin@gamil.com</p>
        </div>
      </div>
    </div>

    <div class="column">
      <div class="card">
        <img src="/img/bot.jpg" alt="John" style="width: 100%" />
        <div class="container">
          <h2>John Doe</h2>
          <p class="title">Designer</p>
          <p>Some text that describes me lorem ipsum ipsum lorem.</p>
          <p>john@example.com</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>
<style scoped>
body {
  font-family: Arial, Helvetica, sans-serif;
  margin: 0;
}

html {
  box-sizing: border-box;
}

*,
*:before,
*:after {
  box-sizing: inherit;
}

.column {
  float: left;
  width: 33.3%;
  margin-bottom: 16px;
  padding: 0 8px;
}

.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  margin: 8px;
}

.about-section {
  padding: 50px;
  text-align: center;
  color: white;
}

.container {
  padding: 0 16px;
}

.container::after,
.row::after {
  content: "";
  clear: both;
  display: table;
}

.title {
  color: grey;
}

.button {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #94af60;
  text-align: center;
  cursor: pointer;
  width: 100%;
}

.button:hover {
  background-color: #555;
}

@media screen and (max-width: 650px) {
  .column {
    width: 100%;
    display: block;
  }
}
</style>
