<script setup lang="ts">
// import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
import TitleView from './views/TitleView.vue'
import EmbeddingOverviewBox from './components/EmbeddingOverviewBox.vue'
import GeoNetworkBox from './components/GeoNetworkBox.vue'
import CityScaleFeatsBox from './components/CityScaleFeatsBox.vue'
import { ref } from 'vue'
import { useCityPicFeatStore } from '@/stores/cityPicFeat'

const cityPicFeatsData = useCityPicFeatStore()

// const sel_shcow_view = ref(-1) // 0散点图 1地图
function set_show_view(target: number) {
  cityPicFeatsData.main_sel_show_view = target
}
</script>

<template>
  <header>
    <TitleView />
  </header>
  <main :class="{ full_show: cityPicFeatsData.main_sel_show_view != -1 }">
    <div class="left_content">
      <div class="top_bar"></div>
      <div
        class="embedding_view_box"
        :class="{ full_show: cityPicFeatsData.main_sel_show_view == 0 }"
      >
        <EmbeddingOverviewBox />
      </div>
      <div
        class="geo_network_view_box"
        :class="{ full_show: cityPicFeatsData.main_sel_show_view == 1 }"
      >
        <GeoNetworkBox />
      </div>
    </div>
    <div class="right_content">
      <CityScaleFeatsBox />
    </div>
    <div class="window_show_nav">
      <button
        :class="{ sel_show_window: cityPicFeatsData.main_sel_show_view == 0 }"
        @click="set_show_view(0)"
      >
        EO
      </button>
      <button
        :class="{ sel_show_window: cityPicFeatsData.main_sel_show_view == 1 }"
        @click="set_show_view(1)"
      >
        GNV
      </button>
      <button
        :class="{ sel_show_window: cityPicFeatsData.main_sel_show_view == -1 }"
        @click="set_show_view(-1)"
      >
        ALL
      </button>
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
main.full_show .left_content {
  width: calc(100% - 16px * 2);
  padding-right: 16px;
}
main.full_show .right_content {
  width: 0;
  overflow: hidden;
  display: none;
}

.left_content .embedding_view_box {
  height: 567px;
  width: 100%;
  padding-bottom: 16px;
}
.left_content .geo_network_view_box {
  width: 100%;
  height: calc(100% - 567px - 16px);
}
main.full_show .left_content:has(.embedding_view_box.full_show) .geo_network_view_box,
main.full_show .left_content:has(.geo_network_view_box.full_show) .embedding_view_box {
  display: none;
}
main.full_show .left_content .embedding_view_box.full_show,
main.full_show .left_content .geo_network_view_box.full_show {
  height: calc(100% - 16px);
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
