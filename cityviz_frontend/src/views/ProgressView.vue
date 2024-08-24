<script setup lang="ts">
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
import { computed } from 'vue'

const cityPicFeatsData = useCityPicFeatStore()

const now_show_progress = computed(() => {
  return (cityPicFeatsData.now_loading_progress / 13) * 100
})
</script>

<template>
  <div class="loading_view_box">
    <div class="loading_title">
      <div class="loading_content">Loading...</div>
      <div class="progress_show_place">
        <div class="progress_bar">
          <div class="now_progress" :style="{ width: `${now_show_progress}%` }"></div>
        </div>
        <div class="progress_num">{{ now_show_progress.toFixed(2) + '%' }}</div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.loading_view_box {
  position: absolute;
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;

  background-color: rgb(27, 33, 52);

  z-index: 599;
}
.loading_view_box .loading_title {
  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;
}
.loading_view_box .loading_title > div {
  padding: 10px;
}
.loading_view_box .loading_title .loading_content {
  font-size: 72px;
  color: #fff;
}
.loading_view_box .loading_title .progress_show_place {
  display: flex;
  flex-direction: row;

  align-items: center;
  justify-content: center;
}
.loading_view_box .loading_title .progress_show_place > div {
  padding: 0 10px;
}
.loading_view_box .loading_title .progress_show_place > .progress_bar {
  width: 500px;
  height: 10px;
  background-color: #fff;
  border: 2px solid #000;
  border-radius: 5px;

  text-align: left;
  justify-content: left;
  padding: 0;
  overflow: hidden;
}
.loading_view_box .loading_title .progress_show_place > .progress_bar > .now_progress {
  background-color: #00d2fc;
  height: 100%;
  /* width: 50%; */
  width: 0%;

  transition: width ease 300ms;
}
/* #00d2fc */
.loading_view_box .loading_title .progress_show_place > .progress_num {
  font-size: 32px;
  color: #fff;
}
</style>
