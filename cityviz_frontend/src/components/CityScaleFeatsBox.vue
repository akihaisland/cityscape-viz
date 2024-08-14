<script setup lang="ts">
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
import HistgramChartSvg from './HistgramChartSvg.vue'
import { computed, ref } from 'vue'

const cityPicFeatsData = useCityPicFeatStore()
const feats_show = ref([true, false, false, false, true, false])
const city_item_if_show = computed(() => {
  for (let i = 0; i < feats_show.value.length; i += 1) {
    if (feats_show.value[i]) return true
  }
  return false
})
function get_city_feat_data(city_idx: number, feat_idx: number) {
  if (feats_show.value[feat_idx]) {
    if (feat_idx == 0) {
      if (cityPicFeatsData.std_cities_feats == undefined) return [] as number[]
      const res = cityPicFeatsData.std_cities_feats.cities_street_scale[city_idx]
      if (res != undefined) return res
      else return [] as number[]
    } else if (feat_idx == 4) {
      if (cityPicFeatsData.std_cities_feats == undefined) return [] as number[]
      const res = cityPicFeatsData.std_cities_feats.cities_greenery[city_idx]
      if (res != undefined) return res
      else return [] as number[]
    }
  } else return [] as number[]
}

const filter_show_items_name = [
  'Street scale',
  'Building color',
  'Facade material',
  'Architectural style',
  'Greenery',
  'Urban sign'
]
function switch_filter_choose(filter_item_idx: number) {
  feats_show.value[filter_item_idx] = !feats_show.value[filter_item_idx]
}
</script>

<template>
  <div class="city_scale_feats_box">
    <div class="city_scale_feats_box_title">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
      >
        <path
          d="M13.0769 7.4591C13.0769 7.18679 12.9136 7.00771 12.7216 6.89048L3.91725 1.49417C3.84617 1.4231 3.70494 1.4231 3.56186 1.4231C3.06525 1.4231 2.9231 1.77848 2.9231 2.06186V12.7843C2.9231 13.1388 3.06525 13.4231 3.56186 13.4231C3.70402 13.4231 3.77509 13.4231 3.91725 13.352L12.7216 8.02587C12.9136 7.9114 13.0769 7.68894 13.0769 7.4591Z"
          fill="#1A2134"
        />
      </svg>
      <span class="title_content"> Geographic network visualization </span>
      <div class="city_filter_box">
        <span class="filter_title"> Cities </span>

        <span class="filter_selection">
          <span> all </span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <g clip-path="url(#clip0_4011_3497)">
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M9.41086 13.0892C9.56713 13.2454 9.77906 13.3332 10 13.3332C10.221 13.3332 10.4329 13.2454 10.5892 13.0892L15.3034 8.37501C15.4552 8.21784 15.5392 8.00733 15.5373 7.78884C15.5354 7.57034 15.4477 7.36133 15.2932 7.20682C15.1387 7.05232 14.9297 6.96468 14.7112 6.96278C14.4927 6.96088 14.2822 7.04487 14.125 7.19667L10 11.3217L5.87503 7.19667C5.71786 7.04487 5.50736 6.96088 5.28886 6.96278C5.07036 6.96468 4.86135 7.05232 4.70685 7.20682C4.55234 7.36133 4.4647 7.57034 4.4628 7.78884C4.4609 8.00733 4.5449 8.21784 4.6967 8.37501L9.41086 13.0892Z"
                fill="#999999"
              />
            </g>
            <defs>
              <clipPath id="clip0_4011_3497">
                <rect width="20" height="20" fill="white" />
              </clipPath>
            </defs>
          </svg>
        </span>
      </div>
    </div>
    <div class="hist_filter_chosens_box">
      <div
        class="chosen_item"
        v-for="(filter_show_item_name, filter_show_item_idx) in filter_show_items_name"
        :key="filter_show_item_idx"
        @click="switch_filter_choose(filter_show_item_idx)"
      >
        <div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            v-show="feats_show[filter_show_item_idx]"
          >
            <rect width="20" height="20" rx="4" fill="#47F6E4" />
            <path
              d="M1.2348 9.99999C1.2348 9.99999 5.76151 13.7028 6.21119 16.852C6.21119 16.852 12.1469 7.13537 18.7421 6.266C18.7421 6.266 16.7335 4.80225 17.393 2.48874C17.393 2.48874 13.7357 2.85367 6.84072 13.5559L3.60923 8.07053L1.2348 9.99999Z"
              fill="white"
            />
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            v-show="!feats_show[filter_show_item_idx]"
          >
            <rect x="0.5" y="0.5" width="19" height="19" rx="3.5" stroke="#DFE1E5" />
          </svg>
          <span> {{ filter_show_item_name }}</span>
        </div>
      </div>
    </div>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      :viewBox="`0 0 0 0`"
      width="0"
      height="0"
      style="position: absolute"
    >
      <defs>
        <linearGradient id="histMyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color: #2d87aa; stop-opacity: 1" />
          <stop offset="100%" style="stop-color: #18263a; stop-opacity: 1" />
        </linearGradient>
      </defs>
    </svg>
    <div class="city_scale_feats_res_box" v-show="city_item_if_show">
      <div
        class="city_feats_item"
        v-for="(city_name, city_idx) in cityPicFeatsData.cities_names"
        :key="city_idx"
      >
        <div class="city_feats_item_title">{{ city_name }}</div>
        <div class="city_feats_item_hists">
          <div class="hist_graph_box" v-show="feats_show[0]">
            <HistgramChartSvg
              :show_data="get_city_feat_data(city_idx, 0)"
              :graph_title="'Street Scale'"
            />
          </div>
          <div class="hist_graph_box" v-show="feats_show[4]">
            <HistgramChartSvg
              :show_data="get_city_feat_data(city_idx, 4)"
              :graph_title="'Greenery'"
            />
          </div>
          <!-- <div class="hist_graph_box">
            <HistgramChartSvg
              :show_data="get_city_feat_data(city_idx, 0)"
              :graph_title="'Street Scale'"
            />
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.city_scale_feats_box {
  width: 100%;
  height: 100%;
  background: #fff;
}

.city_scale_feats_box_title {
  width: calc(100% - 16px * 2);
  height: 36px;
  padding: 0 16px;
  padding-bottom: 8px;

  display: flex;
  flex-direction: row;
  justify-content: left;
  align-items: center;

  border-bottom: 1px solid var(--gray, #dfe1e5);
}

.city_scale_feats_box_title > svg {
  width: 16px;
  height: 16px;
}
.city_scale_feats_box_title > .title_content {
  color: var(--black, #1a2134);

  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;

  padding: 0 10px;
  width: calc(100% - 20px - 16px - 142px);
}

.city_scale_feats_box_title .city_filter_box {
  width: 142px;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.city_scale_feats_box_title .city_filter_box .filter_title {
  color: var(--black, #1a2134);

  /* title_text */
  font-family: Inter;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  padding-right: 10px;
}
.city_scale_feats_box_title .city_filter_box .filter_selection {
  display: flex;
  width: 70px;
  padding: 4px 8px;
  justify-content: space-between;
  align-items: center;

  border-radius: 4px;
  border: 1px solid var(--gray, #dfe1e5);
  cursor: pointer;
}
.city_scale_feats_box_title .city_filter_box .filter_selection > span {
  color: var(--black, #1a2134);

  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.city_scale_feats_box_title .city_filter_box .filter_selection > svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* 下面的区域 */
.hist_filter_chosens_box {
  padding: 12px 0;
  text-align: center;
}
.hist_filter_chosens_box .chosen_item {
  display: inline-block;
  width: 175px;
  cursor: pointer;
  user-select: none;
}
.hist_filter_chosens_box .chosen_item div {
  width: calc(100% - 24px);
  display: flex;
  padding: 4px 12px;
  align-items: center;
  gap: 4px;
}

.hist_filter_chosens_box .chosen_item svg {
  width: 20px;
  height: 20px;
}
.hist_filter_chosens_box .chosen_item span {
  color: var(--black, #1a2134);

  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  user-select: none;

  padding-left: 4px;
}

.city_scale_feats_res_box {
  width: 100%;
  height: calc(100% - 81px - 44px);
  border-radius: 4px;

  /* background-color: azure; */
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
<style scoped>
.city_scale_feats_res_box::-webkit-scrollbar {
  width: 10px;
}
.city_scale_feats_res_box::-webkit-scrollbar-thumb {
  background-color: #b6b6b6;
  border-radius: 10px;
  transition: background-color 0.2s ease;
}

.city_scale_feats_res_box::-webkit-scrollbar-thumb:hover {
  background-color: #a8a8a8;
}

.city_scale_feats_res_box::-webkit-scrollbar-track {
  background-color: #e1e1e1;
  border-radius: 10px;
}

.city_scale_feats_res_box > .city_feats_item {
  padding: 0 40px;
}
.city_scale_feats_res_box > .city_feats_item .city_feats_item_title {
  width: 100%;
  color: var(--black, #1a2134);

  /* body_text_semibold */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;

  padding-bottom: 8px;
}
.city_scale_feats_res_box > .city_feats_item > .city_feats_item_hists {
  width: 100%;
}
.city_scale_feats_res_box > .city_feats_item .hist_graph_box {
  width: calc(100% / 3 - 4px);
  padding: 2px;
  padding-bottom: 5px;

  display: inline-block;
}
</style>
