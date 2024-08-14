<script setup lang="ts">
// import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
import TitleView from './views/TitleView.vue'
import EmbeddingOverviewBox from './components/EmbeddingOverviewBox.vue'
import GeoNetworkBox from './components/GeoNetworkBox.vue'
import CityScaleFeatsBox from './components/CityScaleFeatsBox.vue'
import { ref } from 'vue'

const test1 = ref(0)
</script>

<template>
  <header>
    <TitleView />
  </header>
  <main>
    <div class="left_content">
      <div class="top_bar"></div>
      <div class="embedding_view_box">
        <EmbeddingOverviewBox />
      </div>
      <div class="geo_network_view_box">
        <GeoNetworkBox :test_data="test1" />
      </div>
    </div>
    <div class="right_content">
      <CityScaleFeatsBox />
    </div>
    <div class="window_show_nav">
      <button @click="test1 += 1">EO</button>
      <button>GNV</button>
      <button class="sel_show_window">ALL</button>
    </div>
  </main>
</template>

<style scoped>
header {
  width: 400px;
  height: 100%;
}
main {
  width: calc(100% - 400px);
  height: 100%;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

main .left_content {
  padding: 16px;
  padding-right: 0;
  padding-top: 56px;
  height: calc(100% - 56px - 16px);
  width: calc(100% - 602px - 16px * 3);
}
main .right_content {
  padding: 16px;
  width: 602px;
  height: calc(100% - 32px);
}

.left_content .embedding_view_box {
  height: 567px;
  width: 100%;
  /* background-color: aqua; */
  padding-bottom: 16px;
}
.left_content .geo_network_view_box {
  width: 100%;
  height: calc(100% - 567px - 16px);
  /* background-color: antiquewhite; */
}

/* 展示不同窗口的导航 */
.window_show_nav {
  display: inline-flex;
  padding: 8px 16px;
  align-items: center;
  gap: 8px;
  justify-content: space-between;

  border-radius: 4px 22px 22px 4px;
  background: var(--Grays-Black, #000);

  position: absolute;
  right: calc(602px + 32px);
  top: 0;
}
.window_show_nav button {
  display: flex;
  padding: 4px 8px;
  justify-content: center;
  align-items: center;
  gap: 10px;
  color: var(--white, #fff);

  /* body_text_semibold */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.window_show_nav button.sel_show_window {
  border-radius: 4px;
  background: var(--green, #47f6e4);
}
</style>
