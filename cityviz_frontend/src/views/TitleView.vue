<script setup lang="ts">
import { computed, ref } from 'vue'
import NetworkGraphBox from '../components/NetworkGraphBox.vue'
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
import { transform } from 'typescript'

const cityPicFeatsData = useCityPicFeatStore()
const now_show_filter_box = ref(false) // 是否展示过滤的盒子
// 修改culgroup的呈现形式
function switch_culture_group() {
  cityPicFeatsData.cul_group_status = 1 - cityPicFeatsData.cul_group_status
}
function switch_show_content(target_content: number) {
  if (target_content == cityPicFeatsData.now_show_status && target_content == 1) {
    cityPicFeatsData.cul_group_status = 1 - cityPicFeatsData.cul_group_status
  } else {
    cityPicFeatsData.now_show_status = target_content
    now_show_filter_box.value = false
  }
}
const cities_colors_str = computed(() => {
  const res = [] as string[]
  cityPicFeatsData.cities_colors.forEach((city_color) => {
    res.push(`hsla(${city_color.h}, ${city_color.s}%, ${city_color.l}%, ${city_color.a})`)
  })
  return res
})

// 选择城市的filter box
const city_search_content = ref('')
const city_sel_status = (city_idx: number) => {
  if (cityPicFeatsData.sel_show_cities == undefined) return false
  if (cityPicFeatsData.sel_show_cities.length <= city_idx) return false
  else return cityPicFeatsData.sel_show_cities[city_idx]
}
const search_cities_res = computed(() => {
  const res = [] as number[]
  cityPicFeatsData.cities_names.forEach((city_name, city_idx) => {
    if (city_name.includes(city_search_content.value)) {
      res.push(city_idx)
    }
  })
  return res
})
function switch_city_show_status(city_idx: number) {
  cityPicFeatsData.sel_show_cities[city_idx] = !cityPicFeatsData.sel_show_cities[city_idx]
}
// 选择文化圈的filter box
const cul_groups_search_content = ref('')
const cul_groups_sel_status = (city_idx: number) => {
  if (cityPicFeatsData.sel_show_culture_groups == undefined) return false
  if (cityPicFeatsData.sel_show_culture_groups.length <= city_idx) return false
  else return cityPicFeatsData.sel_show_culture_groups[city_idx]
}
const search_cul_groups_res = computed(() => {
  const res = [] as number[]
  cityPicFeatsData.culture_groups_names.forEach((cul_group_name, cul_group_idx) => {
    if (cul_group_name.includes(cul_groups_search_content.value)) {
      res.push(cul_group_idx)
    }
  })
  return res
})
function switch_cul_groups_show_status(cul_group_idx: number) {
  if (cul_group_idx == -1) cul_group_idx = cityPicFeatsData.culture_groups_names.length - 1
  cityPicFeatsData.sel_show_culture_groups[cul_group_idx] =
    !cityPicFeatsData.sel_show_culture_groups[cul_group_idx]
}
const cul_groups_colors_str = computed(() => {
  const res = [] as string[]
  cityPicFeatsData.culture_groups_colors.forEach((cul_group_color) => {
    res.push(
      `hsla(${cul_group_color.h}, ${cul_group_color.s}%, ${cul_group_color.l}%, ${cul_group_color.a})`
    )
  })
  return res
})

function switch_show_filter_box() {
  now_show_filter_box.value = !now_show_filter_box.value
}

function switch_filter_all() {
  let target_state = true
  if (cityPicFeatsData.now_show_status == 0) {
    cityPicFeatsData.sel_show_cities.forEach((if_show) => {
      if (if_show) target_state = false
    })
    for (let i = 0; i < cityPicFeatsData.sel_show_cities.length; i += 1) {
      cityPicFeatsData.sel_show_cities[i] = target_state
    }
  } else {
    cityPicFeatsData.sel_show_culture_groups.forEach((if_show) => {
      if (if_show) target_state = false
    })
    for (let i = 0; i < cityPicFeatsData.sel_show_culture_groups.length; i += 1) {
      cityPicFeatsData.sel_show_culture_groups[i] = target_state
    }
  }
}
</script>

<template>
  <div class="main_content">
    <div class="title_pos">
      <div class="logo_box"></div>
      <div class="title_content">CityViz</div>
    </div>
    <div class="middle_content">
      <div class="data_analysis_box">
        <div class="box_title">Data Analysis & Overview</div>
        <div class="box_content">
          Enbedding, Lengedn, Network, Cityscape and etc. <br /><br />
          Enbedding, Lengedn, Network, Cityscape and etc. <br />
          Enbedding, Lengedn, Network, Cityscape and etc. <br />
          Enbedding, Lengedn, Network, Cityscape and etc.
        </div>
      </div>
      <div class="view_sel_box">
        <div
          class="view_sel_item"
          :class="{ sel_show_item: cityPicFeatsData.now_show_status == 1 }"
        >
          <button class="view_sel_btn" @click="switch_show_content(1)">
            <span class="view_img">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 48 48"
                fill="none"
              >
                <path
                  d="M17.4682 32.017C18.3155 32.8643 19.3023 33.5296 20.4012 33.9944C21.539 34.4757 22.7475 34.7197 23.9931 34.7197C25.2924 34.7197 26.5487 34.455 27.7272 33.9329C28.6205 33.5371 29.4346 33.0089 30.1569 32.359C30.2182 32.3748 30.2813 32.3828 30.3446 32.3827C30.7583 32.3827 31.0936 32.0474 31.0936 31.6337C31.0936 31.2201 30.7583 30.8847 30.3446 30.8847C30.1542 30.8847 29.9806 30.9559 29.8484 31.0729C29.5107 30.8416 28.8749 30.4882 27.8445 30.2043C28.2924 29.0396 28.6912 27.5143 28.7244 25.7317H32.738C32.7002 27.1063 32.3385 28.4602 31.6858 29.6619C31.6226 29.7782 31.6656 29.9237 31.782 29.9869C31.8378 30.0172 31.9035 30.0241 31.9644 30.0061C32.0254 29.988 32.0767 29.9465 32.107 29.8907C32.8357 28.5493 33.2209 27.0282 33.2209 25.492C33.2209 25.3597 33.1136 25.2523 32.9812 25.2523H15.0051C14.8728 25.2523 14.7655 25.3597 14.7655 25.492C14.7655 26.7377 15.0095 27.9461 15.4907 29.0839C15.9555 30.1828 16.6208 31.1696 17.4682 32.017H17.4682ZM15.2481 25.7317H19.2618C19.2951 27.5143 19.6939 29.0396 20.1418 30.2043C18.5152 30.6525 17.8723 31.2739 17.8316 31.3145C17.7381 31.4081 17.7376 31.5604 17.8312 31.6539C17.8534 31.6763 17.8799 31.694 17.909 31.7061C17.9381 31.7182 17.9694 31.7244 18.0009 31.7244C18.062 31.7244 18.123 31.7011 18.1697 31.6544C18.1733 31.6508 18.5437 31.2944 19.4401 30.942C19.6804 30.8475 19.974 30.7478 20.324 30.6538C20.5535 31.1911 20.7846 31.6334 20.9767 31.9671C21.5214 32.9133 22.137 33.67 22.7265 34.1488C18.5778 33.5445 15.364 30.0178 15.2481 25.7317L15.2481 25.7317ZM23.7535 34.2004C23.1658 34.021 22.2571 33.2308 21.3921 31.7279C21.2162 31.4224 21.0064 31.0223 20.7963 30.5389C21.559 30.3718 22.5358 30.2424 23.7534 30.2273V34.2004L23.7535 34.2004ZM24.2328 30.2273C25.4505 30.2424 26.4272 30.3718 27.19 30.5389C26.9798 31.0223 26.77 31.4224 26.5942 31.7279C25.7291 33.2308 24.8205 34.021 24.2328 34.2004V30.2273V30.2273ZM23.7535 29.7479C22.4699 29.7631 21.4343 29.8999 20.6101 30.087C20.1709 28.9603 19.7749 27.474 19.7413 25.7317H23.7535V29.7479ZM28.5462 30.942C29.0693 31.1476 29.4129 31.3545 29.6092 31.4918C29.6002 31.5385 29.5956 31.5861 29.5956 31.6337C29.5953 31.7956 29.6478 31.9532 29.745 32.0826C28.48 33.1843 26.9174 33.9019 25.2623 34.1467C25.851 33.6679 26.4657 32.912 27.0096 31.967C27.2017 31.6333 27.4328 31.1911 27.6622 30.6538C28.0123 30.7479 28.3059 30.8475 28.5462 30.942ZM27.3762 30.087C26.552 29.8999 25.5163 29.7631 24.2328 29.7479V25.7317H28.245C28.2113 27.474 27.8154 28.9603 27.3762 30.087ZM21.2368 24.2337H33.2208V23.994C33.2208 22.7468 32.8949 21.571 32.3031 20.6833C31.9163 20.1031 31.4449 19.6879 30.9273 19.4609C31.4055 19.151 31.7228 18.613 31.7228 18.002C31.7228 17.0438 30.9433 16.2643 29.9851 16.2643C29.027 16.2643 28.2475 17.0438 28.2475 18.002C28.2475 18.613 28.5648 19.151 29.043 19.4609C28.5255 19.688 28.054 20.1031 27.6672 20.6833C27.4173 21.0582 27.215 21.4847 27.0644 21.946C26.9145 21.0425 26.6651 20.2131 26.3273 19.5157C25.9262 18.6876 25.4289 18.105 24.8794 17.8043C25.3887 17.501 25.7307 16.945 25.7307 16.3105C25.7307 15.3523 24.9512 14.5728 23.9931 14.5728C23.0349 14.5728 22.2554 15.3523 22.2554 16.3105C22.2554 16.945 22.5975 17.501 23.1067 17.8043C22.5572 18.105 22.06 18.6876 21.6589 19.5157C21.3211 20.2131 21.0716 21.0425 20.9218 21.946C20.7712 21.4847 20.5689 21.0583 20.319 20.6833C19.9322 20.1031 19.4608 19.688 18.9432 19.4609C19.4214 19.1511 19.7387 18.613 19.7387 18.002C19.7387 17.0439 18.9592 16.2643 18.001 16.2643C17.0429 16.2643 16.2634 17.0438 16.2634 18.002C16.2634 18.6131 16.5807 19.151 17.0589 19.4609C16.5414 19.688 16.0699 20.1031 15.6831 20.6833C15.0913 21.5711 14.7654 22.7468 14.7654 23.994V24.2337H21.2367L21.2368 24.2337ZM28.7268 18.002C28.7268 17.3081 29.2913 16.7437 29.9851 16.7437C30.679 16.7437 31.2435 17.3081 31.2435 18.002C31.2435 18.6958 30.679 19.2603 29.9851 19.2603C29.2913 19.2603 28.7268 18.6958 28.7268 18.002ZM28.0661 20.9492C28.586 20.1692 29.2676 19.7397 29.9851 19.7397C30.7026 19.7397 31.3842 20.1692 31.9042 20.9492C32.4065 21.7027 32.6989 22.6913 32.7372 23.7543H27.2331C27.2713 22.6913 27.5637 21.7027 28.0661 20.9492ZM16.7428 18.002C16.7428 17.3081 17.3073 16.7437 18.0011 16.7437C18.695 16.7437 19.2594 17.3081 19.2594 18.002C19.2594 18.6958 18.695 19.2603 18.0011 19.2603C17.3073 19.2603 16.7428 18.6958 16.7428 18.002ZM15.2491 23.7543C15.2873 22.6913 15.5797 21.7027 16.082 20.9492C16.602 20.1692 17.2836 19.7397 18.0011 19.7397C18.7186 19.7397 19.4002 20.1692 19.9202 20.9492C20.4225 21.7027 20.7148 22.6913 20.7531 23.7543H15.2491ZM22.7348 16.3105C22.7348 15.6166 23.2993 15.0521 23.9931 15.0521C24.687 15.0521 25.2515 15.6166 25.2515 16.3105C25.2515 17.0043 24.687 17.5688 23.9931 17.5688C23.2993 17.5688 22.7348 17.0043 22.7348 16.3105ZM22.0903 19.7246C22.614 18.6435 23.2897 18.0481 23.9931 18.0481C24.6965 18.0481 25.3723 18.6435 25.8959 19.7246C26.4191 20.8047 26.7188 22.2278 26.7473 23.7543H21.239C21.2674 22.2278 21.5672 20.8047 22.0903 19.7246ZM24.6994 18.6873L23.9919 19.252L23.2714 18.6862C23.1673 18.6044 23.0167 18.6225 22.9349 18.7266C22.8532 18.8307 22.8713 18.9814 22.9754 19.0631L23.7534 19.6742V21.0384C23.7534 21.1708 23.8608 21.2781 23.9931 21.2781C24.1255 21.2781 24.2328 21.1708 24.2328 21.0384V19.673L24.9984 19.0619C25.1019 18.9794 25.1188 18.8286 25.0362 18.7251C24.9537 18.6217 24.8029 18.6048 24.6994 18.6873ZM18.7144 20.2469L18.0069 20.8115L17.2864 20.2457C17.1823 20.1639 17.0316 20.1821 16.9499 20.2862C16.8681 20.3902 16.8862 20.5409 16.9903 20.6227L17.7684 21.2337V22.5192C17.7684 22.6516 17.8757 22.7589 18.0081 22.7589C18.1404 22.7589 18.2477 22.6516 18.2477 22.5192V21.2326L19.0134 20.6215C19.1168 20.5389 19.1337 20.3881 19.0512 20.2847C18.9686 20.1812 18.8178 20.1643 18.7144 20.2469H18.7144ZM30.6984 20.2469L29.9909 20.8115L29.2704 20.2457C29.1663 20.164 29.0157 20.1821 28.9339 20.2862C28.8522 20.3903 28.8703 20.5409 28.9744 20.6227L29.7524 21.2338V22.5192C29.7524 22.6516 29.8598 22.7589 29.9921 22.7589C30.1245 22.7589 30.2318 22.6516 30.2318 22.5192V21.2326L30.9974 20.6215C31.1008 20.539 31.1178 20.3882 31.0352 20.2847C30.9526 20.1813 30.8018 20.1643 30.6984 20.2469ZM26.2775 12.2203C22.8632 11.5602 19.5075 12.4184 16.9074 14.3233C16.8447 14.2885 16.7769 14.2638 16.7065 14.2502C16.3378 14.179 15.9811 14.4201 15.9098 14.7888C15.8386 15.1574 16.0797 15.5141 16.4484 15.5854C16.8171 15.6567 17.1737 15.4156 17.245 15.0469C17.2682 14.9276 17.2589 14.8043 17.218 14.6898C19.7995 12.8084 23.0301 12.0807 26.1865 12.691C27.7134 12.9862 29.1366 13.5714 30.4165 14.4305C31.653 15.2604 32.7048 16.3098 33.5428 17.5493C34.3807 18.7889 34.9623 20.1561 35.2715 21.6128C35.5916 23.1207 35.6042 24.6595 35.309 26.1864C35.0138 27.7134 34.4285 29.1365 33.5695 30.4165C32.7395 31.653 31.6902 32.7048 30.4506 33.5427C29.2111 34.3806 27.8439 34.9623 26.3872 35.2715C24.8793 35.5915 23.3405 35.6042 21.8135 35.309C20.2866 35.0137 18.8634 34.4285 17.5835 33.5694C16.347 32.7395 15.2952 31.6902 14.4573 30.4506C13.6194 29.211 13.0377 27.8439 12.7285 26.3871C12.4084 24.8792 12.3958 23.3404 12.691 21.8135C12.9751 20.3444 13.5287 18.9691 14.3366 17.7258C14.3632 17.6849 14.3902 17.6442 14.4174 17.6037C14.441 17.5738 14.457 17.5386 14.4643 17.5012C14.4895 17.3708 14.4042 17.2446 14.2738 17.2194C14.1687 17.1991 14.0665 17.2505 14.0175 17.3395C13.9897 17.381 13.9619 17.4226 13.9346 17.4646C13.1167 18.7234 12.5229 20.1579 12.2204 21.7225C10.9626 28.2282 15.2168 34.5218 21.7225 35.7796C28.2282 37.0373 34.5218 32.7831 35.7796 26.2774C37.0375 19.7717 32.7832 13.4781 26.2775 12.2203L26.2775 12.2203Z"
                  fill="white"
                  stroke="white"
                />
              </svg>
            </span>
            <span class="view_btn_detail">
              <div class="view_btn_title">Cultural Groups</div>
              <div class="view_btn_desc">Display data at the cultural group level</div>
            </span>
          </button>
          <div class="city_filter_btn_box">
            <button class="city_sel_btn" @click="switch_show_filter_box">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M19.0909 6.54545H4.90909C4.58182 6.54545 4.36364 6.32727 4.36364 6C4.36364 5.67273 4.58182 5.45454 4.90909 5.45454H19.0909C19.4182 5.45454 19.6364 5.67273 19.6364 6C19.6364 6.32727 19.4182 6.54545 19.0909 6.54545ZM19.0909 10.5818H12C11.6727 10.5818 11.4545 10.3636 11.4545 10.0364C11.4545 9.70909 11.6727 9.49091 12 9.49091H19.0909C19.4182 9.49091 19.6364 9.70909 19.6364 10.0364C19.6364 10.3636 19.4182 10.5818 19.0909 10.5818ZM19.0909 14.5091H12C11.6727 14.5091 11.4545 14.2909 11.4545 13.9636C11.4545 13.6364 11.6727 13.4182 12 13.4182H19.0909C19.4182 13.4182 19.6364 13.6364 19.6364 13.9636C19.6364 14.2909 19.4182 14.5091 19.0909 14.5091ZM19.0909 18.5455H4.90909C4.58182 18.5455 4.36364 18.2182 4.36364 18C4.36364 17.7818 4.58182 17.4545 4.90909 17.4545H19.0909C19.4182 17.4545 19.6364 17.6727 19.6364 18C19.6364 18.3273 19.4182 18.5455 19.0909 18.5455Z"
                  fill="#47F6E4"
                />
                <path
                  d="M5.12726 9.38182L8.72726 11.5636C8.94544 11.6727 9.05453 11.7818 9.05453 12C9.05453 12.2182 8.94544 12.3273 8.83635 12.4364L5.23635 14.6182C5.12726 14.7273 5.01817 14.7273 4.90908 14.7273C4.90908 14.7273 4.79999 14.6182 4.6909 14.6182C4.47272 14.5091 4.36362 14.4 4.36362 14.1818V9.81818C4.36362 9.6 4.47272 9.38182 4.58181 9.38182C4.79999 9.27273 4.90908 9.27273 5.12726 9.38182Z"
                  fill="#47F6E4"
                />
              </svg>
            </button>
            <div
              class="city_filter_box"
              v-show="now_show_filter_box && cityPicFeatsData.now_show_status == 1"
            >
              <div class="filter_box_title" @click="switch_filter_all">Legend</div>
              <form class="search_input_box">
                <input type="text" placeholder="city" v-model="cul_groups_search_content" />
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
                  v-for="(cul_group_idx, cul_group_show_idx) in search_cul_groups_res"
                  :key="cul_group_show_idx"
                  :class="{ sel_item: cul_groups_sel_status(cul_group_idx) }"
                  @click="switch_cul_groups_show_status(cul_group_idx)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="17"
                    viewBox="0 0 16 17"
                    fill="none"
                  >
                    <circle
                      cx="8"
                      cy="8.5"
                      r="8"
                      :fill="cul_groups_colors_str[cul_group_show_idx]"
                    />
                  </svg>
                  <span class="item_name">{{
                    cityPicFeatsData.culture_groups_names[cul_group_show_idx]
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          class="view_sel_item"
          :class="{ sel_show_item: cityPicFeatsData.now_show_status == 0 }"
        >
          <button class="view_sel_btn" @click="switch_show_content(0)">
            <span class="view_img"
              ><svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 48 48"
                fill="none"
              >
                <path
                  d="M14.8474 34.1521H13.2203V14.6271C13.2203 14.1956 13.3917 13.7817 13.6969 13.4766C14.002 13.1714 14.4159 13 14.8474 13H24.6099C25.0415 13 25.4553 13.1714 25.7605 13.4766C26.0656 13.7817 26.237 14.1956 26.237 14.6271V34.1521H24.6099V14.6271H14.8474V34.1521ZM32.7454 23.5761H34.3725V34.1521H32.7454V23.5761ZM12.8135 35.7792C12.5978 35.7792 12.3909 35.6935 12.2383 35.5409C12.0857 35.3884 12 35.1814 12 34.9657C12 34.7499 12.0857 34.543 12.2383 34.3904C12.3909 34.2379 12.5978 34.1521 12.8135 34.1521H34.3725C34.5882 34.1521 34.7952 34.2379 34.9477 34.3904C35.1003 34.543 35.186 34.7499 35.186 34.9657C35.186 35.1814 35.1003 35.3884 34.9477 35.5409C34.7952 35.6935 34.5882 35.7792 34.3725 35.7792H12.8135Z"
                  fill="white"
                />
                <path
                  d="M35.4821 23.6314C35.5817 23.6703 35.6726 23.7284 35.7497 23.8024C35.8268 23.8765 35.8886 23.965 35.9315 24.0629C35.9744 24.1608 35.9976 24.2662 35.9998 24.373C36.002 24.4799 35.9831 24.5862 35.9442 24.6857C35.9053 24.7853 35.8472 24.8763 35.7732 24.9534C35.6991 25.0305 35.6106 25.0922 35.5127 25.1352C35.4148 25.1781 35.3094 25.2013 35.2026 25.2034C35.0957 25.2056 34.9894 25.1867 34.8899 25.1478L25.1225 21.3348C24.9242 21.2544 24.7657 21.0991 24.681 20.9027C24.5964 20.7062 24.5926 20.4844 24.6703 20.2851C24.7481 20.0858 24.9012 19.9252 25.0965 19.838C25.2918 19.7508 25.5136 19.744 25.7139 19.8191L35.4829 23.6314H35.4821ZM28.6874 26.2713C28.9032 26.2713 29.1101 26.3571 29.2627 26.5096C29.4152 26.6622 29.5009 26.8691 29.5009 27.0849C29.5009 27.3007 29.4152 27.5076 29.2627 27.6601C29.1101 27.8127 28.9032 27.8984 28.6874 27.8984H25.417C25.2012 27.8984 24.9943 27.8127 24.8417 27.6601C24.6891 27.5076 24.6034 27.3007 24.6034 27.0849C24.6034 26.8691 24.6891 26.6622 24.8417 26.5096C24.9943 26.3571 25.2012 26.2713 25.417 26.2713H28.6874ZM28.6874 29.5255C28.9032 29.5255 29.1101 29.6112 29.2627 29.7638C29.4152 29.9164 29.5009 30.1233 29.5009 30.3391C29.5009 30.5548 29.4152 30.7618 29.2627 30.9143C29.1101 31.0669 28.9032 31.1526 28.6874 31.1526H25.417C25.2012 31.1526 24.9943 31.0669 24.8417 30.9143C24.6891 30.7618 24.6034 30.5548 24.6034 30.3391C24.6034 30.1233 24.6891 29.9164 24.8417 29.7638C24.9943 29.6112 25.2012 29.5255 25.417 29.5255H28.6874ZM18.9151 26.0167C18.9151 26.2325 18.8294 26.4394 18.6768 26.592C18.5243 26.7445 18.3173 26.8302 18.1016 26.8302C17.8858 26.8302 17.6789 26.7445 17.5263 26.592C17.3737 26.4394 17.288 26.2325 17.288 26.0167V24.3896C17.288 24.1738 17.3737 23.9669 17.5263 23.8144C17.6789 23.6618 17.8858 23.5761 18.1016 23.5761C18.3173 23.5761 18.5243 23.6618 18.6768 23.8144C18.8294 23.9669 18.9151 24.1738 18.9151 24.3896V26.0167ZM18.9151 20.3219C18.9151 20.5377 18.8294 20.7446 18.6768 20.8972C18.5243 21.0497 18.3173 21.1354 18.1016 21.1354C17.8858 21.1354 17.6789 21.0497 17.5263 20.8972C17.3737 20.7446 17.288 20.5377 17.288 20.3219V18.6948C17.288 18.479 17.3737 18.2721 17.5263 18.1195C17.6789 17.967 17.8858 17.8813 18.1016 17.8813C18.3173 17.8813 18.5243 17.967 18.6768 18.1195C18.8294 18.2721 18.9151 18.479 18.9151 18.6948V20.3219ZM22.1693 20.3219C22.1693 20.5377 22.0836 20.7446 21.931 20.8972C21.7784 21.0497 21.5715 21.1354 21.3557 21.1354C21.14 21.1354 20.9331 21.0497 20.7805 20.8972C20.6279 20.7446 20.5422 20.5377 20.5422 20.3219V18.6948C20.5422 18.479 20.6279 18.2721 20.7805 18.1195C20.9331 17.967 21.14 17.8813 21.3557 17.8813C21.5715 17.8813 21.7784 17.967 21.931 18.1195C22.0836 18.2721 22.1693 18.479 22.1693 18.6948V20.3219ZM22.1693 26.0167C22.1693 26.2325 22.0836 26.4394 21.931 26.592C21.7784 26.7445 21.5715 26.8302 21.3557 26.8302C21.14 26.8302 20.9331 26.7445 20.7805 26.592C20.6279 26.4394 20.5422 26.2325 20.5422 26.0167V24.3896C20.5422 24.1738 20.6279 23.9669 20.7805 23.8144C20.9331 23.6618 21.14 23.5761 21.3557 23.5761C21.5715 23.5761 21.7784 23.6618 21.931 23.8144C22.0836 23.9669 22.1693 24.1738 22.1693 24.3896V26.0167ZM18.9151 34.9657H17.288V29.5255H22.4134V34.9657H20.7863V31.1526H18.9151V34.9657Z"
                  fill="white"
                />
              </svg>
            </span>
            <span class="view_btn_detail">
              <div class="view_btn_title">Cities</div>
              <div class="view_btn_desc">Display data at the city level</div>
            </span>
          </button>
          <div class="city_filter_btn_box">
            <button class="city_sel_btn" @click="switch_show_filter_box">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M19.0909 6.54545H4.90909C4.58182 6.54545 4.36364 6.32727 4.36364 6C4.36364 5.67273 4.58182 5.45454 4.90909 5.45454H19.0909C19.4182 5.45454 19.6364 5.67273 19.6364 6C19.6364 6.32727 19.4182 6.54545 19.0909 6.54545ZM19.0909 10.5818H12C11.6727 10.5818 11.4545 10.3636 11.4545 10.0364C11.4545 9.70909 11.6727 9.49091 12 9.49091H19.0909C19.4182 9.49091 19.6364 9.70909 19.6364 10.0364C19.6364 10.3636 19.4182 10.5818 19.0909 10.5818ZM19.0909 14.5091H12C11.6727 14.5091 11.4545 14.2909 11.4545 13.9636C11.4545 13.6364 11.6727 13.4182 12 13.4182H19.0909C19.4182 13.4182 19.6364 13.6364 19.6364 13.9636C19.6364 14.2909 19.4182 14.5091 19.0909 14.5091ZM19.0909 18.5455H4.90909C4.58182 18.5455 4.36364 18.2182 4.36364 18C4.36364 17.7818 4.58182 17.4545 4.90909 17.4545H19.0909C19.4182 17.4545 19.6364 17.6727 19.6364 18C19.6364 18.3273 19.4182 18.5455 19.0909 18.5455Z"
                  fill="#47F6E4"
                />
                <path
                  class="anime_path"
                  d="M5.12726 9.38182L8.72726 11.5636C8.94544 11.6727 9.05453 11.7818 9.05453 12C9.05453 12.2182 8.94544 12.3273 8.83635 12.4364L5.23635 14.6182C5.12726 14.7273 5.01817 14.7273 4.90908 14.7273C4.90908 14.7273 4.79999 14.6182 4.6909 14.6182C4.47272 14.5091 4.36362 14.4 4.36362 14.1818V9.81818C4.36362 9.6 4.47272 9.38182 4.58181 9.38182C4.79999 9.27273 4.90908 9.27273 5.12726 9.38182Z"
                  fill="#47F6E4"
                />
              </svg>
            </button>

            <div
              class="city_filter_box"
              v-show="now_show_filter_box && cityPicFeatsData.now_show_status == 0"
            >
              <div class="filter_box_title" @click="switch_filter_all">Legend</div>
              <form class="search_input_box">
                <input type="text" placeholder="city" v-model="city_search_content" />
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
                  :class="{ sel_item: city_sel_status(city_idx) }"
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
      </div>
    </div>
    <div class="network_graph_box">
      <div class="box_title">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="17"
          viewBox="0 0 16 17"
          fill="none"
        >
          <g clip-path="url(#clip0_2_254)">
            <path
              d="M15.3076 10.2283C15.3076 9.95601 15.1443 9.77693 14.9523 9.6597L6.14795 4.26339C6.07688 4.19231 5.93565 4.19231 5.79257 4.19231C5.29595 4.19231 5.1538 4.5477 5.1538 4.83108V15.5535C5.1538 15.908 5.29595 16.1923 5.79257 16.1923C5.93472 16.1923 6.0058 16.1923 6.14795 16.1212L14.9523 10.7951C15.1443 10.6806 15.3076 10.4582 15.3076 10.2283Z"
              fill="white"
            />
          </g>
          <defs>
            <clipPath id="clip0_2_254">
              <rect width="16" height="16" fill="white" transform="translate(0 0.5)" />
            </clipPath>
          </defs>
        </svg>
        <span>Network Visualization</span>
      </div>
      <div class="box_content">
        <NetworkGraphBox />
      </div>
    </div>
  </div>
</template>

<style scoped>
.main_content {
  width: 100%;
  height: 100%;
  background: #000;
  position: relative;
}
.title_pos {
  padding: 24px 32px;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  /* align-content: center; */
}
.title_pos .logo_box {
  width: 72px;
  height: 72px;
  background-color: #d9d9d9;
  border-radius: 4px;
}
.title_pos .title_content {
  padding: 0 10px;
  width: calc(100% - 72px);

  color: white;
  font-family: 'inter';
  font-size: 24px;
  font-weight: 600;

  display: flex;
  flex-direction: row;
  justify-content: left;
  /* align-content: center; */
  align-items: center;

  height: 22px;
}

/* 下面盒子的内容 */
.network_graph_box {
  padding: 15px 32px;
  width: calc(100% - 32px * 2);
  height: 426px;
}
.network_graph_box .box_title svg {
  width: 16px;
  height: 16px;
}
.network_graph_box .box_title span {
  width: calc(100% - 16px);
  padding-left: 10px;

  color: var(--white, #fff);

  /* body_text_semibold */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.network_graph_box .box_content {
  width: 100%;
  height: calc(100% - 22px - 8px);
  padding-top: 8px;
}

/* 中间的部分 */
.middle_content {
  width: 100%;
  height: calc(100% - 120px - 456px);
}
/* 数据分析部分 */
.data_analysis_box {
  width: calc(100% - 32px * 2);
  height: 127px;

  padding: 32px;
}
.data_analysis_box .box_title {
  color: var(--white, #fff);

  /* nav_bar title */
  font-family: Inter;
  font-size: 18px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;

  height: 22px;
  padding-bottom: 4px;
}
.data_analysis_box .box_content {
  width: 100%;
  height: calc(100% - 24px);

  color: var(--white, #fff);

  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
/* view选择部分 */
.view_sel_box {
  width: calc(100% - 40px);
  padding-left: 40px;
}
.view_sel_box .view_sel_item {
  width: 100%;
  height: 48px;
  padding: 24px 0;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.view_sel_box .view_sel_item .view_sel_btn {
  width: calc(100% - 40px);
  height: 100%;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.view_sel_box .view_sel_item .view_sel_btn .view_img {
  width: 48px;
  height: 48px;
}
.view_sel_box .view_sel_item .view_sel_btn .view_btn_detail {
  padding: 0 16px;
  padding-right: 0;
  width: calc(100% - 48px - 8px * 2);
  text-align: left;
}
.view_sel_box .view_sel_item .view_sel_btn .view_btn_detail .view_btn_title {
  color: var(--white, #fff);

  /* nav_bar title */
  font-family: Inter;
  font-size: 18px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.view_sel_box .view_sel_item .view_sel_btn .view_btn_detail .view_btn_desc {
  color: var(--white, #fff);

  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}

.view_sel_box .view_sel_item .city_filter_btn_box {
  padding: 3px 8px;
  width: 24px;
  height: 100%;
  position: relative;
}
.view_sel_box .view_sel_item .city_filter_btn_box button {
  width: 24px;
  height: 24px;
  display: none;
}
.view_sel_box .view_sel_item .city_filter_btn_box button svg {
  width: 100%;
  height: 100%;
}

.view_sel_box .view_sel_item.sel_show_item .view_sel_btn .view_btn_title,
.view_sel_box .view_sel_item.sel_show_item .view_sel_btn .view_btn_desc {
  color: #47f6e4;
}
.view_sel_box .view_sel_item.sel_show_item .view_sel_btn .view_img {
  border-radius: 50%;
  background-color: #47f6e4;
}
.view_sel_box .view_sel_item.sel_show_item .city_filter_btn_box button {
  display: block;
}
</style>
<style scoped>
.city_filter_box {
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
  left: 50px;
  top: -50px;
  /* top: 0; */

  z-index: 999;
}
.city_filter_box .filter_box_title {
  display: flex;
  padding: 8px 16px;
  align-items: center;
  gap: 10px;
  align-self: stretch;

  border-radius: 4px 4px 0px 0px;
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
.city_filter_box .search_input_box {
  display: flex;
  width: calc(184px - 32px);
  padding: 8px 16px;
  justify-content: space-between;
  align-items: center;

  border-radius: 4px;
  border: 1px solid var(--gray, #dfe1e5);
}
.city_filter_box .search_input_box > input {
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
.city_filter_box .search_input_box button {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
.city_filter_box .search_input_box button > svg {
  width: 100%;
  height: 100%;
}
.city_filter_box .filter_list {
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
.city_filter_box .filter_list .filter_item {
  display: flex;
  align-items: center;
  gap: 8px;
  align-self: stretch;

  cursor: pointer;
}
.city_filter_box .filter_list .filter_item.sel_item > span {
  color: #000;
}
.city_filter_box .filter_list .filter_item:not(.sel_item) {
  color: var(--dark_gray, #999);
}
.city_filter_box .filter_list .filter_item > svg {
  width: 16px;
  height: 16px;
}
.city_filter_box .filter_list .filter_item > span {
  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;

  user-select: none;
}

/* 滚轮 */
.city_filter_box .filter_list::-webkit-scrollbar {
  width: 10px;
}
.city_filter_box .filter_list::-webkit-scrollbar-thumb {
  background-color: #b6b6b6;
  border-radius: 10px;
  transition: background-color 0.2s ease;
}

.city_filter_box .filter_list::-webkit-scrollbar-thumb:hover {
  background-color: #a8a8a8;
}

.city_filter_box .filter_list::-webkit-scrollbar-track {
  background-color: #e1e1e1;
  border-radius: 10px;
}
</style>
