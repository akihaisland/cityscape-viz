<script setup lang="ts">
import * as d3 from 'd3'
import { computed, onMounted, ref, watch } from 'vue'
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
const cityPicFeatsData = useCityPicFeatStore()

function hsl_color_obj2str(color_obj: { h: number; s: number; l: number; a: number }) {
  if (color_obj == undefined) return `hsla(180, 100%, 100%, 0)`
  else return `hsla(${color_obj.h}, ${color_obj.s}%, ${color_obj.l}%, ${color_obj.a})`
}

function hsls2rgbs(color_obj: { h: number; s: number; l: number; a: number }) {
  let r, g, b

  function hue2Rgb(p: number, q: number, t: number) {
    if (t < 0) t += 1
    if (t > 1) t -= 1
    if (t < 1 / 6) return p + (q - p) * 6 * t
    if (t < 1 / 2) return q
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6
    return p
  }
  let h = 0.5,
    s = 1,
    l = 1,
    a = 0
  if (color_obj != undefined) {
    h = color_obj.h / 360
    s = color_obj.s / 100
    l = color_obj.l / 100
    a = color_obj.a
  }
  let q = l < 0.5 ? l * (1 + s) : l + s - l * s
  let p = 2 * l - q
  r = hue2Rgb(p, q, h + 1 / 3)
  g = hue2Rgb(p, q, h)
  b = hue2Rgb(p, q, h - 1 / 3)

  return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255), a: a }
}
function hsla_color2rgba_str(color_obj: { h: number; s: number; l: number; a: number }) {
  const rgba_obj = hsls2rgbs(color_obj)
  // return `rgba(${rgba_obj.r}, ${rgba_obj.g}, ${rgba_obj.b}, ${rgba_obj.a})`
  return `rgba(${rgba_obj.r}, ${rgba_obj.g}, ${rgba_obj.b})`
  // return '#1772F6aa'
}
function hsla_color2hex_str(color_obj: { h: number; s: number; l: number; a: number }) {
  const rgba_obj = hsls2rgbs(color_obj)
  const toHex = (color: number) => {
    let hex = color.toString(16)
    return hex.length == 1 ? '0' + hex : hex
  }
  return '#' + toHex(rgba_obj.r) + toHex(rgba_obj.g) + toHex(rgba_obj.b)
}

function show_node_color(node_idx: number) {
  const color_obj = cityPicFeatsData.tsne_pts_color[node_idx]
  if (color_obj == undefined) {
    return {
      // node_color: `hsla(180, 100%, 100%, 0)`
      node_color: `rgba(0,0,0,0)`
    }
  } else if (cityPicFeatsData.cul_group_status == 1 && cityPicFeatsData.now_show_status == 1) {
    return {
      // node_color: `hsla(180, 100%, 100%, 0)`
      node_color: `rgba(0,0,0,0)`
    }
  }
  // return {
  //   node_color: `hsla(${color_obj.h}, ${color_obj.s}%, ${color_obj.l}%, ${color_obj.a})`
  // }
  // return { node_color: hsla_color2rgba_str(color_obj) }
  return { node_color: hsla_color2hex_str(color_obj) }
}

const zoom_rate = ref(150)
function zoom_up(e: MouseEvent) {
  e.stopPropagation()
  e.preventDefault()
  zoom_rate.value /= 0.9
}
function zoom_down(e: MouseEvent) {
  e.stopPropagation()
  e.preventDefault()
  zoom_rate.value *= 0.9
}
function handle_wheel(e: WheelEvent) {
  if (e.deltaY > 0) zoom_down(e)
  else zoom_up(e)
}
const box_pos = ref([0, 0])
const now_box_status = ref(0)
function switch_now_box_status(target_status: number) {
  if (now_box_status.value == target_status && now_box_status.value) {
    if (target_status == 3) {
      now_box_status.value = 0
      return
    }
  }
  now_box_status.value = target_status
}
function start_move(e: MouseEvent) {
  if (now_box_status.value != 3 && now_box_status.value != 0) return
  e.stopPropagation()
  e.preventDefault()
  const start_mouse = [e.clientX, e.clientY]
  const start_pos = [box_pos.value[0], box_pos.value[1]]

  function handleMouseMove(e1: MouseEvent) {
    e.stopPropagation()
    e.preventDefault()
    box_pos.value[0] = start_pos[0] + (e1.clientX - start_mouse[0]) / (zoom_rate.value / 100)
    box_pos.value[1] = start_pos[1] + (e1.clientY - start_mouse[1]) / (zoom_rate.value / 100)
  }
  function handleMoveEnd() {
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMoveEnd)
  }
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMoveEnd)
}

const cul_groups_center = ref([] as { pos: number[]; color: string }[])
function draw_scatter_KDE() {
  const svg = d3.select('#embeddings_bg_board')
  svg.selectAll('*').remove()
  cul_groups_center.value = []
  if (cityPicFeatsData.now_show_status == 0) return

  // 根据模式修改透明度
  const tmp_cul_groups_center = [] as { pos: number[]; color: string }[]
  let layer_opacity = 0.08
  if (cityPicFeatsData.cul_group_status == 1) layer_opacity = 0.2
  cityPicFeatsData.cul_group2data_idx.forEach((cul_group_datas_idx, cul_idx) => {
    if (!cityPicFeatsData.sel_show_culture_groups[cul_idx]) return

    const cul_group_datas = [] as [number, number][]
    cul_group_datas_idx.forEach((data_idx) => {
      cul_group_datas.push([
        cityPicFeatsData.std_tsne_pts[data_idx][0],
        cityPicFeatsData.std_tsne_pts[data_idx][1]
      ])
    })
    const svg_size = 400
    let densityProgress = d3
      .contourDensity()
      .x((d) => d[0] * (svg_size - 200) + 100)
      .y((d) => d[1] * (svg_size - 200) + 100)
      .size([svg_size, svg_size])
      .thresholds(10)
      .bandwidth(10)(cul_group_datas)

    let cul_group_color_obj = cityPicFeatsData.culture_groups_colors[cul_idx]

    if (cityPicFeatsData.cul_group_status == 1) {
      // 计算质心
      const cul_group_mid = [0, 0]
      densityProgress[densityProgress.length - 1].coordinates[0][0].forEach((node_pos) => {
        cul_group_mid[0] += node_pos[0]
        cul_group_mid[1] += node_pos[1]
      })
      cul_group_mid[0] /= densityProgress[densityProgress.length - 1].coordinates[0][0].length
      cul_group_mid[1] /= densityProgress[densityProgress.length - 1].coordinates[0][0].length
      tmp_cul_groups_center.push({
        pos: cul_group_mid,
        // color: hsl_color_obj2str(cul_group_color_obj)
        // color: hsla_color2rgba_str(cul_group_color_obj)
        color: hsla_color2hex_str(cul_group_color_obj)
      })

      // 修改颜色
      cul_group_color_obj.s *= 1.1
      if (cul_group_color_obj.s > 100) cul_group_color_obj.s = 100
    }
    // const cul_group_color_str = hsl_color_obj2str(cul_group_color_obj)
    // const cul_group_color_str = hsla_color2rgba_str(cul_group_color_obj)
    const cul_group_color_str = hsla_color2hex_str(cul_group_color_obj)
    svg
      .append('g')
      .attr('stroke-linejoin', 'round')
      .selectAll()
      .data(densityProgress)
      .join('path')
      .attr('fill', (d, i) => {
        // if (i % 3 == 0) return cul_group_color_str
        // else return 'none'
        return cul_group_color_str
      })
      .attr('fill-opacity', layer_opacity)
      .attr('stroke', (d, i) => {
        return 'none'
      })
      .attr('stroke-width', 1)
      .attr('d', d3.geoPath())
    // console.log('kde_data', densityProgress)
  })
  // 保存质心坐标
  cul_groups_center.value = tmp_cul_groups_center
}
// const cul_groups_centers = computed(() => {
//   const res = []
//   // const mids = [] as number[][]
//   const cul_data_mid = new Array<number>(cityPicFeatsData.culture_groups_names.length).fill(-1)
//   cityPicFeatsData.cul_group2data_idx.forEach((datas, cul_idx) => {
//     const diss = [] as number[]
//     datas.forEach((data1_idx, idx_in_cul_group) => {
//       const data1_pos = cityPicFeatsData.tsne_pos[data1_idx]
//       diss.push(0)
//       datas.forEach((data2_idx) => {
//         const data2_pos = cityPicFeatsData.tsne_pos[data2_idx]
//         diss.push(
//           Math.sqrt(
//             Math.pow(data1_pos[0] - data2_pos[0], 2) + Math.pow(data1_pos[1] - data2_pos[1], 2)
//           )
//         )
//       })
//     })
//   })
//   return []
// })

const nodes2show = computed(() => {
  const res = [] as { x: number; y: number; color: string; data_idx: number }[]
  cityPicFeatsData.std_tsne_pts.forEach((std_tsne_pt, data_idx) => {
    const city_idx = cityPicFeatsData.idx2city_idxs[data_idx]
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[city_idx]
    if (cityPicFeatsData.now_show_status == 0 && !cityPicFeatsData.sel_show_cities[city_idx]) return
    if (cityPicFeatsData.now_show_status == 1 && !cityPicFeatsData.sel_show_culture_groups[cul_idx])
      return
    res.push({
      x: std_tsne_pt[0],
      y: std_tsne_pt[1],
      color: show_node_color(data_idx).node_color,
      data_idx: data_idx
    })
  })
  return res
})

watch(
  () => cityPicFeatsData.sel_show_culture_groups,
  () => {
    draw_scatter_KDE()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.now_show_status,
  () => {
    draw_scatter_KDE()
  }
)
watch(
  () => cityPicFeatsData.cul_group_status,
  () => {
    draw_scatter_KDE()
  }
)

// Create the horizontal and vertical scales.
onMounted(async () => {
  await cityPicFeatsData.init_all_feats()
})

// 返回视图主页面
function back2home_view() {
  zoom_rate.value = 100
  box_pos.value = [0, 0]
}

// 保存截图
function download_now_view() {
  const outer_box = document.getElementById('scatter_outer_box') as HTMLElement
  const outer_box_rect = outer_box.getBoundingClientRect()
  const zoom_std_rate = zoom_rate.value / 100

  const svg_box_size = [outer_box_rect.width - 2, outer_box_rect.height - 2]
  const svg_pos = [
    svg_box_size[0] / 2 - 200 * zoom_std_rate + box_pos.value[0] * zoom_std_rate,
    svg_box_size[1] / 2 - 200 * zoom_std_rate + box_pos.value[1] * zoom_std_rate
  ]
  let svgData =
    `<svg xmlns="http://www.w3.org/2000/svg" version="1.1" ` +
    'viewBox=' +
    `"${0} ${0} ` +
    `${svg_box_size[0]} ` +
    `${svg_box_size[1]}" ` +
    `style="width: ${svg_box_size[0]}px; height: ${svg_box_size[1]}px;"` +
    `>` +
    `<g style="transform: translate(${svg_pos[0]}px, ${svg_pos[1]}px) scale(${zoom_rate.value}%);" >`

  // 填充内容
  const nodes_layer = document.getElementById('embeddings_place_board') as HTMLElement
  const nodes_bg_layer = document.getElementById('embeddings_bg_board') as HTMLElement
  const cul_groups_mids_layer = document.getElementById('embeddings_mids_board') as HTMLElement
  if (cityPicFeatsData.now_show_status == 0) {
    // 城市数据
    svgData += nodes_layer.innerHTML
  } else {
    // 文化圈数据
    svgData += nodes_bg_layer.innerHTML
    if (cityPicFeatsData.cul_group_status == 1) {
      svgData += cul_groups_mids_layer.innerHTML
    } else {
      svgData += nodes_layer.innerHTML
    }
  }
  svgData += '</g></svg>'

  const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  const now_timestamp = new Date().getTime()
  a.download = `image-${now_timestamp}.svg`
  a.click()
  // window.open(url, '_blank')
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="embed_overview_box">
    <div class="embed_overview_box_title">
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
      <span class="title_content"> Embedding Overview </span>
      <div class="tools_bar">
        <!-- <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M8.00447 4.96716C8.19044 4.96716 8.36879 5.04104 8.50028 5.17254C8.63178 5.30403 8.70566 5.48238 8.70566 5.66835V7.30445H10.3418C10.5277 7.30445 10.7061 7.37832 10.8376 7.50982C10.9691 7.64131 11.0429 7.81966 11.0429 8.00563C11.0429 8.1916 10.9691 8.36994 10.8376 8.50144C10.7061 8.63294 10.5277 8.70682 10.3418 8.70682H8.70566V10.3429C8.70566 10.5289 8.63178 10.7072 8.50028 10.8387C8.36879 10.9702 8.19044 11.0441 8.00447 11.0441C7.8185 11.0441 7.64016 10.9702 7.50866 10.8387C7.37716 10.7072 7.30329 10.5289 7.30329 10.3429V8.70682H5.66719C5.48122 8.70682 5.30287 8.63294 5.17138 8.50144C5.03988 8.36994 4.966 8.1916 4.966 8.00563C4.966 7.81966 5.03988 7.64131 5.17138 7.50982C5.30287 7.37832 5.48122 7.30445 5.66719 7.30445H7.30329V5.66835C7.30329 5.48238 7.37716 5.30403 7.50866 5.17254C7.64016 5.04104 7.8185 4.96716 8.00447 4.96716Z"
              fill="#1A2134"
            />
            <path
              d="M3.51595 12.4409C4.61354 13.5385 6.07709 14.1932 7.6269 14.2798C9.17671 14.3663 10.7041 13.8788 11.9171 12.9103L16.7375 17.7297C16.8704 17.8536 17.0462 17.921 17.2279 17.9178C17.4095 17.9146 17.5828 17.841 17.7113 17.7126C17.8398 17.5841 17.9134 17.4108 17.9166 17.2291C17.9198 17.0475 17.8524 16.8716 17.7285 16.7387L12.909 11.9183C13.6697 10.9664 14.1385 9.8147 14.259 8.60219C14.3794 7.38968 14.1463 6.16822 13.5878 5.08528C13.0293 4.00233 12.1693 3.1042 11.1116 2.49931C10.0538 1.89442 8.84362 1.60863 7.62703 1.67644C6.41044 1.74425 5.23949 2.16276 4.25553 2.88145C3.27158 3.60015 2.51669 4.58829 2.08199 5.72659C1.6473 6.86489 1.55139 8.10469 1.80585 9.2963C2.0603 10.4879 2.65424 11.5804 3.51595 12.4419V12.4409ZM4.50696 4.5082C3.58581 5.42811 3.06782 6.67627 3.06694 7.97809C3.06607 9.27992 3.58238 10.5288 4.50229 11.4499C5.4222 12.3711 6.67035 12.8891 7.97218 12.8899C9.27401 12.8908 10.5229 12.3745 11.444 11.4546L11.4487 11.4499L11.4524 11.4453C12.346 10.519 12.84 9.27885 12.828 7.99191C12.816 6.70497 12.2991 5.47421 11.3885 4.56472C10.4779 3.65522 9.24652 3.13977 7.95957 3.12937C6.67262 3.11898 5.43306 3.61447 4.5079 4.50913L4.50696 4.5082Z"
              fill="#1A2134"
            />
            <rect
              x="4.57782"
              y="4.57904"
              width="6.4793"
              height="6.4793"
              rx="1.5"
              stroke="#F4F4F4"
            />
          </svg>
        </button>
        <button @click="switch_now_box_status(3)" :class="{ sel_btn: now_box_status == 3 }">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M2 10.3333L7 13.2201V7.44659L2 10.3333ZM18.25 10.3333L13.25 7.44659V13.2201L18.25 10.3333ZM6.5 10.8333H13.75V9.83334H6.5V10.8333Z"
              fill="#1A2134"
            />
            <path
              d="M10.3333 2L7.44656 7L13.2201 7L10.3333 2ZM10.3333 18.25L13.2201 13.25L7.44656 13.25L10.3333 18.25ZM9.83331 6.5L9.83331 13.75L10.8333 13.75L10.8333 6.5L9.83331 6.5Z"
              fill="#1A2134"
            />
          </svg>
        </button>
        <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M17 3.25H14.5V2H17.625C17.7071 2 17.7883 2.01617 17.8642 2.04758C17.94 2.07898 18.0089 2.12502 18.0669 2.18306C18.125 2.2411 18.171 2.30999 18.2024 2.38582C18.2338 2.46165 18.25 2.54292 18.25 2.625V5.75H17V3.25ZM17 14.5H18.25V17.625C18.25 17.7908 18.1842 17.9497 18.0669 18.0669C17.9497 18.1842 17.7908 18.25 17.625 18.25H14.5V17H17V14.5ZM5.75 17V18.25H2.625C2.54292 18.25 2.46165 18.2338 2.38582 18.2024C2.30999 18.171 2.2411 18.125 2.18306 18.0669C2.12502 18.0089 2.07898 17.94 2.04758 17.8642C2.01617 17.7883 2 17.7071 2 17.625V14.5H3.25V17H5.75ZM3.25 3.25V5.75H2V2.625C2 2.54292 2.01617 2.46165 2.04758 2.38582C2.07898 2.30999 2.12502 2.2411 2.18306 2.18306C2.2411 2.12502 2.30999 2.07898 2.38582 2.04758C2.46165 2.01617 2.54292 2 2.625 2H5.82875V3.25H3.25ZM8.25 2H12V3.25H8.25V2ZM8.25 17H12V18.25H8.25V17ZM2 8.25H3.25V12H2V8.25ZM17 8.25H18.25V12H17V8.25Z"
              fill="#1A2134"
            />
          </svg>
        </button>
        <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M16.0062 11.8097C16.6458 11.4413 17.1843 10.9205 17.5739 10.2937C17.9634 9.66682 18.192 8.95335 18.2391 8.2168C18.2391 5.33437 14.6056 3 10.1195 3C5.63349 3 2 5.33437 2 8.2168C2 10.5106 4.29377 12.4491 7.48069 13.1494C6.97643 13.7284 6.29488 14.1245 5.54215 14.276C5.32671 14.2891 5.11106 14.254 4.9109 14.1732C4.71074 14.0925 4.53112 13.9681 4.38511 13.8091L3.67465 14.5196C3.89634 14.7628 4.16576 14.9577 4.46611 15.0921C4.76646 15.2266 5.0913 15.2977 5.42035 15.3011H5.62334C6.83941 15.0446 7.92122 14.3559 8.66817 13.3626C9.1501 13.4163 9.63462 13.4434 10.1195 13.4437H10.7894V17.0975C10.7894 17.2498 11.0127 17.2904 11.0939 17.1584L13.5094 13.464C13.5279 13.4359 13.5538 13.4135 13.5843 13.3992C13.6147 13.3848 13.6485 13.3792 13.682 13.3829L18.0462 14.0629C18.2086 14.0629 18.3203 13.9005 18.1985 13.799L16.0062 11.8097ZM6.56724 11.221C6.56724 10.9368 7.00366 10.6121 7.58218 10.6121C8.1607 10.6121 8.59712 10.9368 8.59712 11.221C8.59712 11.5052 8.1607 11.83 7.58218 11.83C7.00366 11.83 6.56724 11.5052 6.56724 11.221ZM10.1195 12.4288C9.744 12.4288 9.37863 12.4288 9.0234 12.3679C9.20157 12.2334 9.34705 12.0604 9.44898 11.8618C9.55092 11.6632 9.60666 11.4442 9.61206 11.221C9.55097 10.7397 9.30493 10.301 8.92605 9.99791C8.54717 9.69481 8.06519 9.55107 7.58218 9.59712C7.09917 9.55107 6.61719 9.69481 6.23831 9.99791C5.85943 10.301 5.61339 10.7397 5.5523 11.221C5.54731 11.2886 5.54731 11.3564 5.5523 11.424C4.02988 10.6425 3.01494 9.48548 3.01494 8.2168C3.01494 5.94333 6.2729 4.01494 10.1195 4.01494C13.9662 4.01494 17.2241 5.94333 17.2241 8.2168C17.1625 8.83391 16.9435 9.42487 16.5881 9.93311C16.2326 10.4414 15.7527 10.8499 15.1942 11.1195L14.6665 10.6527L11.1345 7.415C11.1093 7.39367 11.0786 7.37999 11.046 7.37557C11.0133 7.37115 10.9801 7.37617 10.9502 7.39005C10.9203 7.40393 10.895 7.42608 10.8773 7.45389C10.8596 7.48169 10.8502 7.51398 10.8503 7.54694V12.4085L10.1195 12.4288Z"
              fill="#1A2134"
            />
          </svg>
        </button>
        <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M2.40625 3.5967C2.40625 2.71527 3.01343 2.00006 3.76174 2.00006H5.73865V3.19859H3.76174C3.67179 3.19859 3.58552 3.24068 3.52191 3.3156C3.45831 3.39053 3.42257 3.49214 3.42257 3.5981V5.92532H2.40625V3.5967ZM18.25 16.6534C18.25 17.5363 17.6428 18.2501 16.8945 18.2501H14.9164V17.0529H16.8933C16.9833 17.0529 17.0695 17.0108 17.1331 16.9359C17.1967 16.861 17.2325 16.7594 17.2325 16.6534V14.3248H18.25V16.6534ZM16.8933 2.00006C17.6428 2.00006 18.2488 2.71527 18.2488 3.5967V5.92671H17.2325V3.5967C17.2325 3.49099 17.1969 3.38958 17.1336 3.3147C17.0702 3.23982 16.9842 3.19756 16.8945 3.19719H14.9176V2.00006H16.8945H16.8933ZM3.76174 18.2501C3.40224 18.2501 3.05747 18.0818 2.80326 17.7824C2.54906 17.483 2.40625 17.0769 2.40625 16.6534V14.3248H3.42257V16.6534C3.42257 16.8741 3.57437 17.0529 3.76174 17.0529H5.73865V18.2501H3.76174Z"
              fill="#1A2134"
            />
            <path
              d="M2 10.5526L5.75 12.7177L5.75 8.38758L2 10.5526ZM17.8437 10.5526L14.0937 8.38758L14.0937 12.7177L17.8437 10.5526ZM5.375 10.9276L14.4687 10.9276L14.4687 10.1776L5.375 10.1776L5.375 10.9276Z"
              fill="#1A2134"
            />
            <path
              d="M10.3388 2L8.17374 5.75L12.5039 5.75L10.3388 2ZM10.3388 18.25L12.5039 14.5L8.17374 14.5L10.3388 18.25ZM9.96381 5.375L9.96381 14.875L10.7138 14.875L10.7138 5.375L9.96381 5.375Z"
              fill="#1A2134"
            />
          </svg>
        </button> -->
        <button @click="download_now_view">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M16.5623 6.04234H13.8573V4.68775C13.8573 3.93927 13.2472 3.33334 12.4987 3.33334H7.08468C6.3362 3.33334 5.73028 3.93945 5.73028 4.68775V6.04234H3.02128C2.2728 6.04234 1.66669 6.64845 1.66669 7.39276V15.5198C1.66669 16.2722 2.2728 16.8742 3.02128 16.8742H16.5623C17.3108 16.8742 17.9167 16.2722 17.9167 15.5198V7.39276C17.9167 6.64827 17.3106 6.04234 16.5623 6.04234ZM3.80222 8.74717C3.42807 8.74717 3.12302 8.44611 3.12302 8.07196C3.12302 7.69781 3.42807 7.39258 3.79823 7.39258C4.17238 7.39258 4.47743 7.69763 4.47743 8.07196C4.47743 8.44629 4.17238 8.74717 3.80222 8.74717ZM9.79368 15.7842C7.42238 15.7842 5.48199 13.844 5.48199 11.4645C5.48199 9.08487 7.41404 7.16098 9.79368 7.16098C12.1733 7.16098 14.1054 9.08487 14.1054 11.4645C14.0972 13.852 12.1733 15.7842 9.79368 15.7842Z"
              fill="#1A2134"
            />
            <path
              d="M9.7937 9.42245C8.66291 9.42245 7.74359 10.3376 7.74359 11.4684C7.74359 12.5992 8.66291 13.5225 9.7937 13.5225C10.9245 13.5225 11.8396 12.6032 11.8438 11.4684C11.8438 10.3378 10.9245 9.42245 9.7937 9.42245Z"
              fill="#1A2134"
            />
          </svg>
        </button>
        <button @click="back2home_view">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M11.4109 16.7113V12.6418H8.85267V16.7222C8.77273 16.7263 8.70896 16.7325 8.64515 16.7325C7.43726 16.7325 6.22872 16.7331 5.02075 16.7325C4.60567 16.7325 4.32655 16.4662 4.32472 16.0253C4.31633 14.351 4.31887 12.6753 4.32656 11.001C4.32656 10.9127 4.39363 10.7998 4.4613 10.7395C5.55449 9.77366 6.65341 8.81399 7.75049 7.85355C8.48076 7.21425 9.21042 6.57489 9.94066 5.93625C9.9974 5.88694 10.0555 5.83907 10.1269 5.77805C10.5627 6.1587 10.9964 6.53722 11.4296 6.91644C12.8586 8.16709 14.2856 9.42047 15.7185 10.6663C15.8725 10.7998 15.9383 10.9353 15.937 11.1509C15.9279 12.7404 15.9305 14.3305 15.9338 15.9192C15.9344 16.2081 15.8667 16.4594 15.6262 16.6189C15.5392 16.677 15.429 16.727 15.3291 16.7277C14.0471 16.7345 12.7651 16.731 11.4838 16.7304C11.4651 16.7304 11.4457 16.7215 11.4109 16.7113ZM13.3362 5.44483C13.3362 4.7733 13.3356 4.15314 13.3362 3.53361C13.3368 3.13798 13.4258 3.0435 13.7977 3.04284C14.3752 3.04284 14.9527 3.0422 15.5303 3.0435C15.8281 3.04425 15.9311 3.15576 15.9318 3.49051C15.9332 4.81639 15.9363 6.14306 15.9279 7.46893C15.9266 7.67361 15.9808 7.80499 16.1322 7.93505C16.7652 8.47586 17.3859 9.03165 18.0098 9.58406C18.3159 9.85517 18.3237 9.9872 18.0659 10.3097C17.9099 10.5054 17.7572 10.7046 17.5999 10.8998C17.4065 11.1413 17.2467 11.1564 17.0153 10.951C14.8 8.9878 12.5846 7.02325 10.3686 5.0594C10.2919 4.99163 10.2133 4.92518 10.1237 4.84712C9.62545 5.28803 9.13107 5.72406 8.63797 6.16142C6.83971 7.75505 5.04139 9.34924 3.24308 10.9428C2.99944 11.1591 2.84804 11.1461 2.64306 10.8914C2.47333 10.6798 2.30489 10.4672 2.13774 10.2535C1.94306 10.0044 1.95083 9.84347 2.18606 9.63337C3.1896 8.74141 4.1958 7.85288 5.20128 6.96301C6.54127 5.77673 7.88259 4.59186 9.22198 3.40355C9.82974 2.8648 10.4215 2.8648 11.0306 3.40764C11.7505 4.049 12.4725 4.68772 13.1937 5.32702C13.2279 5.35721 13.264 5.38522 13.3362 5.44483H13.3362Z"
              fill="#1A2134"
            />
          </svg>
        </button>
        <button @click="zoom_up">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M8.75391 3.59375C10.1328 3.59375 11.4277 4.13086 12.4023 5.10547C13.377 6.08008 13.9141 7.375 13.9141 8.75391C13.9141 10.1328 13.377 11.4277 12.4023 12.4023C11.4277 13.377 10.1328 13.9141 8.75391 13.9141C7.375 13.9141 6.08008 13.377 5.10547 12.4023C4.13086 11.4277 3.59375 10.1309 3.59375 8.75391C3.59375 7.375 4.13086 6.08008 5.10547 5.10547C6.08008 4.13086 7.375 3.59375 8.75391 3.59375ZM8.75391 1.875C6.99414 1.875 5.23242 2.54687 3.89062 3.89062C1.20508 6.57617 1.20508 10.9316 3.89062 13.6191C5.23438 14.9629 6.99414 15.6348 8.75391 15.6348C10.5137 15.6348 12.2754 14.9629 13.6172 13.6191C16.3027 10.9336 16.3027 6.57812 13.6172 3.89062C12.2734 2.54687 10.5137 1.875 8.75391 1.875Z"
              fill="#1A2134"
            />
            <path
              d="M13.6172 12.7578C13.3965 12.7578 13.1777 12.8418 13.0098 13.0097C12.6738 13.3457 12.6738 13.8906 13.0098 14.2265L16.6582 17.875C16.8262 18.0429 17.0469 18.1269 17.2656 18.1269C17.4863 18.1269 17.7051 18.0429 17.873 17.875C18.209 17.539 18.209 16.9941 17.873 16.6582L14.2246 13.0097C14.0566 12.8418 13.8379 12.7578 13.6172 12.7578ZM11.0801 8.14645C10.9238 7.9902 10.709 7.8945 10.4727 7.8945H7.03516C6.56055 7.8945 6.17383 8.27927 6.17383 8.75583C6.17383 8.99411 6.26953 9.20895 6.42578 9.36325C6.58203 9.5195 6.79688 9.6152 7.0332 9.6152H10.4727C10.9473 9.6152 11.334 9.23044 11.334 8.75388C11.334 8.51755 11.2363 8.30075 11.0801 8.14645Z"
              fill="#1A2134"
            />
            <path
              d="M9.36133 6.42575C9.20508 6.2695 8.99023 6.1738 8.75391 6.1738C8.2793 6.1738 7.89258 6.55856 7.89258 7.03513V10.4746C7.89258 10.7129 7.98828 10.9277 8.14453 11.082C8.30078 11.2383 8.51562 11.334 8.75195 11.334C9.22656 11.334 9.61328 10.9492 9.61328 10.4726L9.61523 7.03513C9.61328 6.79684 9.51758 6.582 9.36133 6.42575Z"
              fill="#1A2134"
            />
          </svg>
        </button>
        <button @click="zoom_down">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M8.75391 3.59375C10.1328 3.59375 11.4277 4.13086 12.4023 5.10547C13.377 6.08008 13.9141 7.375 13.9141 8.75391C13.9141 10.1328 13.377 11.4277 12.4023 12.4023C11.4277 13.377 10.1328 13.9141 8.75391 13.9141C7.375 13.9141 6.08008 13.377 5.10547 12.4023C4.13086 11.4277 3.59375 10.1309 3.59375 8.75391C3.59375 7.375 4.13086 6.08008 5.10547 5.10547C6.08008 4.13086 7.375 3.59375 8.75391 3.59375ZM8.75391 1.875C6.99414 1.875 5.23242 2.54687 3.89062 3.89062C1.20508 6.57617 1.20508 10.9316 3.89062 13.6191C5.23438 14.9629 6.99414 15.6348 8.75391 15.6348C10.5137 15.6348 12.2754 14.9629 13.6172 13.6191C16.3027 10.9336 16.3027 6.57812 13.6172 3.89062C12.2734 2.54687 10.5137 1.875 8.75391 1.875Z"
              fill="#1A2134"
            />
            <path
              d="M13.6172 12.7578C13.3965 12.7578 13.1777 12.8418 13.0098 13.0097C12.6738 13.3457 12.6738 13.8906 13.0098 14.2265L16.6582 17.875C16.8262 18.0429 17.0469 18.1269 17.2656 18.1269C17.4863 18.1269 17.7051 18.0429 17.873 17.875C18.209 17.539 18.209 16.9941 17.873 16.6582L14.2246 13.0097C14.0566 12.8418 13.8379 12.7578 13.6172 12.7578ZM11.0801 8.14645C10.9238 7.9902 10.709 7.8945 10.4727 7.8945H7.03516C6.56055 7.8945 6.17383 8.27927 6.17383 8.75583C6.17383 8.99411 6.26953 9.20895 6.42578 9.36325C6.58203 9.5195 6.79688 9.6152 7.0332 9.6152H10.4727C10.9473 9.6152 11.334 9.23044 11.334 8.75388C11.334 8.51755 11.2363 8.30075 11.0801 8.14645Z"
              fill="#1A2134"
            />
          </svg>
        </button>
      </div>
    </div>
    <div
      class="embed_overview_place"
      @mousedown="start_move"
      @wheel="handle_wheel"
      id="scatter_outer_box"
    >
      <div class="zoom_box" :style="{ transform: `scale(${zoom_rate}%)` }">
        <div class="move_box" :style="{ left: box_pos[0] + 'px', top: box_pos[1] + 'px' }">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 400 400"
            id="embeddings_bg_board"
          ></svg>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" id="embeddings_mids_board">
            <circle
              v-for="(node_pos, node_idx) in cul_groups_center"
              :key="node_idx"
              :cx="node_pos.pos[0]"
              :cy="node_pos.pos[1]"
              :fill="node_pos.color"
              stroke="#fff"
              stroke-width="0.6"
              r="2.5"
            />
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 400 400"
            id="embeddings_place_board"
            v-show="
              !(cityPicFeatsData.now_show_status == 1 && cityPicFeatsData.cul_group_status == 1)
            "
          >
            <circle
              v-for="(node_pos_obj, node_idx) in nodes2show"
              :key="node_idx"
              :cx="100 + node_pos_obj.x * 200"
              :cy="100 + node_pos_obj.y * 200"
              :fill="node_pos_obj.color"
              r="0.5"
            />
          </svg>
          <!-- cul_groups_center -->
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.embed_overview_box {
  width: 100%;
  height: 100%;
  background: #fff;
}

.embed_overview_box_title {
  width: 100%;
  height: 20px;
  padding-bottom: 8px;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.embed_overview_box_title > svg {
  width: 16px;
  height: 16px;
}
.embed_overview_box_title > .title_content {
  color: var(--black, #1a2134);

  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;

  padding: 0 10px;
  width: calc(100% - 20px - 16px - 252px);
}

.embed_overview_box_title > .tools_bar {
  width: 252px;

  display: flex;
  flex-direction: row;
  justify-content: right;
  align-items: center;
}
.embed_overview_box_title > .tools_bar button {
  width: 20px;
  height: 20px;
  margin: 0 4px;
}
.embed_overview_box_title > .tools_bar button.sel_btn {
  border-radius: 50%;
  background-color: #cfcecd;
}
.embed_overview_box_title > .tools_bar svg {
  width: 100%;
  height: 100%;
}
</style>
<style scoped>
.embed_overview_place {
  border: 1px solid #8c8c8c;
  width: calc(100% - 2px);
  height: calc(100% - 28px - 2px);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}
.embed_overview_place svg {
  width: 400px;
  height: 400px;
  left: calc(50% - 200px);
  top: calc(50% - 200px);
  position: absolute;
}
.embed_overview_place > .zoom_box {
  width: 100%;
  height: 100%;
  position: relative;
  transform-origin: center center;
}
.embed_overview_place .move_box {
  width: 100%;
  height: 100%;
  position: absolute;
  /* background-color: hsla(hue, saturation, lightness, alpha); */
}
</style>
