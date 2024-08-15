<script setup lang="ts">
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
import HistgramChartSvg from './HistgramChartSvg.vue'
import { computed, ref, watch } from 'vue'

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

// 搜索过滤城市的部分
const if_show_filter_box = ref(false)
watch(
  () => cityPicFeatsData.main_sel_show_view,
  (newVal) => {
    if (newVal != -1) if_show_filter_box.value = false
  }
)
function switch_show_cities_filter() {
  if_show_filter_box.value = !if_show_filter_box.value
}
const cities_data_filter = ref([] as boolean[])
watch(
  () => cityPicFeatsData.cities_names,
  (newVal) => {
    cities_data_filter.value = new Array<boolean>(newVal.length).fill(true)
  }
)
function switch_filter_all() {
  let target_state = true
  cities_data_filter.value.forEach((filter_city) => {
    if (filter_city) target_state = false
  })
  for (let i = 0; i < cities_data_filter.value.length; i += 1) {
    cities_data_filter.value[i] = target_state
  }
}
const cities_search_content = ref('')
const search_cities_res = computed(() => {
  const res = [] as number[]
  for (let i = 0; i < cities_data_filter.value.length; i += 1) {
    if (cityPicFeatsData.cities_names[i].includes(cities_search_content.value)) {
      res.push(i)
    }
  }
  return res
})
const cities_sel_status = (city_idx: number) => {
  if (cities_data_filter.value.length <= city_idx) return false
  else return cities_data_filter.value[city_idx]
}
function switch_city_show_status(city_idx: number) {
  cities_data_filter.value[city_idx] = !cities_data_filter.value[city_idx]
}
const cities_colors_str = computed(() => {
  const res = [] as string[]
  cityPicFeatsData.cities_colors.forEach((city_color) => {
    res.push(`hsla(${city_color.h}, ${city_color.s}%, ${city_color.l}%, ${city_color.a})`)
  })
  return res
})
// 过滤结果
const filter_show_res = computed(() => {
  const res = [] as { name: string; city_idx: number }[]
  cities_data_filter.value.forEach((city_if_show, city_idx) => {
    if (city_if_show) {
      res.push({
        name: cityPicFeatsData.cities_names[city_idx],
        city_idx: city_idx
      })
    }
  })
  return res
})
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

        <span class="filter_selection" @click="switch_show_cities_filter">
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

        <div class="city_filter_sel_box" v-show="if_show_filter_box">
          <div class="filter_box_title" @click="switch_filter_all">Legend</div>
          <form class="search_input_box">
            <input type="text" placeholder="city" v-model="cities_search_content" />
            <button>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
              >
                <path
                  d="M12.9167 11.6667H12.2583L12.025 11.4417C12.8699 10.4617 13.3343 9.21058 13.3333 7.91667C13.3333 6.84535 13.0157 5.7981 12.4205 4.90733C11.8253 4.01656 10.9793 3.3223 9.98954 2.91232C8.99977 2.50235 7.91066 2.39508 6.85993 2.60408C5.8092 2.81309 4.84404 3.32897 4.08651 4.08651C3.32897 4.84404 2.81309 5.8092 2.60408 6.85993C2.39508 7.91066 2.50235 8.99977 2.91232 9.98954C3.3223 10.9793 4.01656 11.8253 4.90733 12.4205C5.7981 13.0157 6.84535 13.3333 7.91667 13.3333C9.25834 13.3333 10.4917 12.8417 11.4417 12.025L11.6667 12.2583V12.9167L15.8333 17.075L17.075 15.8333L12.9167 11.6667ZM7.91667 11.6667C5.84167 11.6667 4.16667 9.99167 4.16667 7.91667C4.16667 5.84167 5.84167 4.16667 7.91667 4.16667C9.99167 4.16667 11.6667 5.84167 11.6667 7.91667C11.6667 9.99167 9.99167 11.6667 7.91667 11.6667Z"
                  fill="#999999"
                />
              </svg>
            </button>
          </form>
          <div class="filter_list">
            <div
              class="filter_item"
              v-for="(city_idx, city_show_idx) in search_cities_res"
              :key="city_show_idx"
              :class="{ sel_item: cities_sel_status(city_idx) }"
              @click="switch_city_show_status(city_idx)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="17"
                viewBox="0 0 16 17"
                fill="none"
              >
                <circle cx="8" cy="8.5" r="8" :fill="cities_colors_str[city_idx]" />
              </svg>
              <span class="item_name">{{ cityPicFeatsData.cities_names[city_idx] }}</span>
            </div>
          </div>
        </div>
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
        v-for="(city_obj, city_show_idx) in filter_show_res"
        :key="city_show_idx"
      >
        <div class="city_feats_item_title">{{ city_obj.name }}</div>
        <div class="city_feats_item_hists">
          <div class="hist_graph_box" v-show="feats_show[0]">
            <HistgramChartSvg
              :show_data="get_city_feat_data(city_obj.city_idx, 0)"
              :graph_title="'Street Scale'"
            />
          </div>
          <div class="hist_graph_box" v-show="feats_show[4]">
            <HistgramChartSvg
              :show_data="get_city_feat_data(city_obj.city_idx, 4)"
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

  position: relative;
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
  user-select: none;
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
<style scoped>
.city_filter_sel_box {
  display: flex;
  width: 216px;
  padding-bottom: 16px;
  flex-direction: column;
  align-items: center;
  gap: 8px;

  border-radius: 4px;
  border: 1px solid var(--Grays-Black, #000);
  background: var(--light_gray, #f4f4f4);

  position: absolute;
  right: 0px;
  top: 50px;
  /* top: 0; */

  z-index: 999;
  overflow: hidden;
}
.city_filter_sel_box .filter_box_title {
  display: flex;
  padding: 8px 16px;
  align-items: center;
  gap: 10px;
  align-self: stretch;

  /* border-radius: 4px 4px 0px 0px; */
  background: var(--Grays-Black, #000);

  color: var(--white, #fff);

  /* title_text */
  font-family: Inter;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;

  user-select: none;
  cursor: pointer;
}
.city_filter_sel_box .search_input_box {
  display: flex;
  width: calc(184px - 32px);
  padding: 8px 16px;
  justify-content: space-between;
  align-items: center;

  border-radius: 4px;
  border: 1px solid var(--gray, #dfe1e5);
}
.city_filter_sel_box .search_input_box > input {
  width: calc(100% - 20px);
  outline: none;
  border: none;
  padding: 0;
  background: none;
  margin: 0;

  color: var(--dark_gray, #999);

  /* tab_text */
  font-family: Inter;
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.city_filter_sel_box .search_input_box button {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
.city_filter_sel_box .search_input_box button > svg {
  width: 100%;
  height: 100%;
}
.city_filter_sel_box .filter_list {
  display: flex;
  width: calc(184px - 10px);
  height: 206px;
  padding: 8px 0px;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;

  overflow-y: auto;
  overflow-x: hidden;
  padding-left: 10px;
}
.city_filter_sel_box .filter_list .filter_item {
  display: flex;
  align-items: center;
  gap: 8px;
  align-self: stretch;

  cursor: pointer;
}
.city_filter_sel_box .filter_list .filter_item.sel_item > span {
  color: #000;
}
.city_filter_sel_box .filter_list .filter_item:not(.sel_item) {
  color: var(--dark_gray, #999);
}
.city_filter_sel_box .filter_list .filter_item > svg {
  width: 16px;
  height: 16px;
}
.city_filter_sel_box .filter_list .filter_item > span {
  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;

  user-select: none;
}

/* 滚轮 */
.city_filter_sel_box .filter_list::-webkit-scrollbar {
  width: 10px;
}
.city_filter_sel_box .filter_list::-webkit-scrollbar-thumb {
  background-color: #b6b6b6;
  border-radius: 10px;
  transition: background-color 0.2s ease;
}

.city_filter_sel_box .filter_list::-webkit-scrollbar-thumb:hover {
  background-color: #a8a8a8;
}

.city_filter_sel_box .filter_list::-webkit-scrollbar-track {
  background-color: #e1e1e1;
  border-radius: 10px;
}
</style>
