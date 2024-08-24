<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import * as turf from '@turf/turf'
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
import CityScaleFeatsBox from './CityScaleFeatsBox.vue'
let map: L.Map
const map_zoom_rate = ref(5)

const if_map_loaded = ref(false)
const cityPicFeatsData = useCityPicFeatStore()
const cities_x = ref([] as number[])
const cities_y = ref([] as number[])

function hsl_color_obj2str(color_obj: { h: number; s: number; l: number; a: number }) {
  if (color_obj == undefined) return `hsla(180, 100%, 100%, 0)`
  else return `hsla(${color_obj.h}, ${color_obj.s}%, ${color_obj.l}%, ${color_obj.a})`
}

const cities_color_after_view = computed(() => {
  const res = [] as { h: number; s: number; l: number; a: number }[]

  const cities_num = cityPicFeatsData.cities2cul_group_idx.length
  for (let c1_idx = 0; c1_idx < cities_num; c1_idx += 1) {
    if (cityPicFeatsData.now_show_status == 0) {
      res.push(cityPicFeatsData.cities_colors[c1_idx])
    } else {
      const cul_idx = cityPicFeatsData.cities2cul_group_idx[c1_idx]
      res.push(cityPicFeatsData.culture_groups_colors[cul_idx])
    }
  }
  return res
})
const cities_grad_color = computed(() => {
  const res = []
  const cities_num = cities_x.value.length
  for (let c1_idx = 0; c1_idx < cities_num; c1_idx += 1) {
    for (let c2_idx = 0; c2_idx < cities_num; c2_idx += 1) {
      if (c1_idx <= c2_idx) continue
      let c1_color_obj = cities_color_after_view.value[c1_idx]
      let c2_color_obj = cities_color_after_view.value[c2_idx]
      const start_pos = [0, 0]
      const end_pos = [100, 100]
      if (cities_x.value[c1_idx] > cities_x.value[c2_idx]) {
        start_pos[0] = 100
        end_pos[0] = 0
      }
      if (cities_y.value[c1_idx] > cities_y.value[c2_idx]) {
        start_pos[1] = 100
        end_pos[1] = 0
      }
      res.push({
        x1: start_pos[0],
        y1: start_pos[1],
        x2: end_pos[0],
        y2: end_pos[1],
        c1: hsl_color_obj2str(c1_color_obj),
        c2: hsl_color_obj2str(c2_color_obj),
        city1: c1_idx,
        city2: c2_idx
      })
    }
  }
  return res
})

// tooltip展示城市数据
const now_hover_node = ref(-1)
let now_hover_pos = [-1, -1]
let node_hover_timer = -1
const hover_node_tooltip_pos = computed(() => {
  if (now_hover_node.value >= 0) {
    const father_ele = document.getElementById('geo_network_outer_box') as HTMLElement
    const father_pos_rect = father_ele.getBoundingClientRect()
    let tooltip_content =
      `City: ${cityPicFeatsData.cities_names[now_hover_node.value]}\n` +
      `Degree Centrality: ${cityPicFeatsData.city_closeness_centrality[now_hover_node.value].toFixed(5)}`
    if (cityPicFeatsData.now_show_status == 1) {
      const now_cul = cityPicFeatsData.cities2cul_group_idx[now_hover_node.value]
      tooltip_content =
        `Culture Group: ${cityPicFeatsData.culture_groups_names[now_cul]}\n` +
        `Degree Centrality: ${cityPicFeatsData.city_closeness_centrality[now_hover_node.value].toFixed(5)}`
    }
    return {
      x: now_hover_pos[0] - father_pos_rect.left,
      y: now_hover_pos[1] - father_pos_rect.top,
      tooltip: tooltip_content
    }
  }
  return { x: -1, y: -1, tooltip: '' }
})
function handle_hover_node(e: MouseEvent, city_idx: number) {
  if (node_hover_timer) clearTimeout(node_hover_timer)
  node_hover_timer = setTimeout(() => {
    now_hover_node.value = city_idx
    now_hover_pos = [e.clientX, e.clientY]
  }, 200)
}
function handle_node_out() {
  if (node_hover_timer) clearTimeout(node_hover_timer)
  now_hover_node.value = -1
}
// edge数据
const now_hover_edge = ref([-1, -1])
let edge_hover_timer = -1
const hover_edge_tooltip_pos = computed(() => {
  const c1 = now_hover_edge.value[0]
  const c2 = now_hover_edge.value[1]
  if (c1 >= 0 && c2 >= 0) {
    const edge_sim =
      (cityPicFeatsData.normalized_cities_conf_matrix[c1][c2] +
        cityPicFeatsData.normalized_cities_conf_matrix[c2][c1]) /
      2
    const father_ele = document.getElementById('geo_network_outer_box') as HTMLElement
    const father_pos_rect = father_ele.getBoundingClientRect()

    const edge_tooltip =
      `City: ${cityPicFeatsData.cities_names[c1]}, ${cityPicFeatsData.cities_names[c2]}\n` +
      `Similarity: ${edge_sim.toFixed(5)}`
    return {
      x: now_hover_pos[0] - father_pos_rect.left,
      y: now_hover_pos[1] - father_pos_rect.top,
      tooltip: edge_tooltip
    }
  }
  return { x: -1, y: -1, tooltip: '' }
})
function handle_hover_edge(e: MouseEvent, c1_idx: number, c2_idx: number) {
  if (edge_hover_timer) clearTimeout(edge_hover_timer)
  edge_hover_timer = setTimeout(() => {
    now_hover_edge.value = [c1_idx, c2_idx]
    now_hover_pos = [e.clientX, e.clientY]
  }, 200)
}
function handle_edge_out() {
  if (edge_hover_timer) clearTimeout(edge_hover_timer)
  now_hover_edge.value = [-1, -1]
}

let svgOverlay: L.SVGOverlay
let svg_edges_overlay: L.SVGOverlay
let svg_cities_names_overlay: L.SVGOverlay
let addded_svg_w = 400
let added_svg_h = 400
const edge_max_w = 5
const edge_min_w = 0.2
const node_max_radius = 1
const node_min_radius = 0.5
const cities_sim_threshold = cityPicFeatsData.cities_sim_threshold
const node_opacity = 0.9
const line_opacity = 0.5

// 获取城市位置 并画出点与线
function reset_cities_client_pos() {
  if (!if_map_loaded.value) return

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    let x_min = 10000,
      x_max = -10000,
      y_min = 10000,
      y_max = -10000
    cityPicFeatsData.cities_pos.forEach((city_pos, city_idx) => {
      const now_pos = map.latLngToContainerPoint([city_pos.lat, city_pos.lon])
      cities_x.value.push(now_pos.x)
      cities_y.value.push(now_pos.y)
    })

    const min_pos = map.latLngToContainerPoint([90, -180])
    x_min = min_pos.x
    y_min = min_pos.y
    const max_pos = map.latLngToContainerPoint([-90, 180])
    x_max = max_pos.x
    y_max = max_pos.y

    added_svg_h = (addded_svg_w * (y_max - y_min)) / (x_max - x_min)
    for (let i = 0; i < cityPicFeatsData.cities_pos.length; i += 1) {
      cities_x.value[i] = ((cities_x.value[i] - x_min) / (x_max - x_min)) * addded_svg_w
      cities_y.value[i] = ((cities_y.value[i] - y_min) / (y_max - y_min)) * added_svg_h
    }
  }
}
function gen_geo_edges_svg_elements() {
  const cities_num = cities_x.value.length
  let inner_content = ''
  const edges_show = [] as number[][]
  for (let c1_idx = 0; c1_idx < cities_num; c1_idx += 1) {
    for (let c2_idx = 0; c2_idx < cities_num; c2_idx += 1) {
      if (c1_idx <= c2_idx) continue
      if (
        cityPicFeatsData.now_show_status == 0 &&
        (!cityPicFeatsData.sel_show_cities[c1_idx] || !cityPicFeatsData.sel_show_cities[c2_idx])
      )
        continue
      const cul1_idx = cityPicFeatsData.cities2cul_group_idx[c1_idx]
      const cul2_idx = cityPicFeatsData.cities2cul_group_idx[c2_idx]
      if (
        cityPicFeatsData.now_show_status == 1 &&
        (!cityPicFeatsData.sel_show_culture_groups[cul1_idx] ||
          !cityPicFeatsData.sel_show_culture_groups[cul2_idx])
      )
        continue

      const start_pos = [cities_x.value[c1_idx], cities_y.value[c1_idx]]
      const end_pos = [cities_x.value[c2_idx], cities_y.value[c2_idx]]
      const mid_pos = [
        (cities_x.value[c1_idx] + cities_x.value[c2_idx]) / 2,
        (cities_y.value[c1_idx] + cities_y.value[c2_idx]) / 2
      ]
      const line_vec = [
        cities_x.value[c1_idx] - cities_x.value[c2_idx],
        cities_y.value[c1_idx] - cities_y.value[c2_idx]
      ]
      const control_pos = [mid_pos[0] + line_vec[1] / 3, mid_pos[1] - line_vec[0] / 3]
      const now_path_d = `M${start_pos[0]} ${start_pos[1]}Q${control_pos[0]} ${control_pos[1]}, ${end_pos[0]} ${end_pos[1]}`
      const stroke_color = `url(#city${c1_idx}-city${c2_idx}_grad_color)`

      const cities_sim =
        (cityPicFeatsData.normalized_cities_conf_matrix[c1_idx][c2_idx] +
          cityPicFeatsData.normalized_cities_conf_matrix[c2_idx][c1_idx]) /
        2
      const now_edge_w = cities_sim * (edge_max_w - edge_min_w) + edge_min_w
      if (cities_sim > cityPicFeatsData.cities_sim_threshold) {
        edges_show.push([c1_idx, c2_idx])
        const edge_id = `geo_edge_n${c1_idx}_${c2_idx}`
        inner_content += `<path d="${now_path_d}" stroke="${stroke_color}" stroke-width="${now_edge_w}" id=${edge_id} fill="none" />`
      }
    }
  }
  return {
    inner_content: inner_content,
    edges_show: edges_show
  }
}
function redraw_edges_by_svg() {
  if (!if_map_loaded.value) return
  if (svg_edges_overlay != undefined) map.removeLayer(svg_edges_overlay)

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    reset_cities_client_pos()
  }

  const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svgElement.setAttribute('viewBox', `0 0 ${addded_svg_w} ${added_svg_h}`)

  const inner_content = gen_geo_edges_svg_elements().inner_content

  svgElement.innerHTML = inner_content
  var latLngBounds = L.latLngBounds([
    [90, 180],
    [-90, -180]
  ])
  // map.fitBounds(latLngBounds)

  svg_edges_overlay = L.svgOverlay(svgElement, latLngBounds, {
    opacity: line_opacity,
    interactive: true
  }).addTo(map)
}
function gen_geo_nodes_svg_elements() {
  const cities_show = [] as number[]
  const max_r_val = Math.max(...cityPicFeatsData.city_closeness_centrality)
  let inner_content = ''
  for (let i = 0; i < cityPicFeatsData.cities_pos.length; i += 1) {
    if (cityPicFeatsData.now_show_status == 0 && !cityPicFeatsData.sel_show_cities[i]) continue
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[i]
    if (cityPicFeatsData.now_show_status == 1 && !cityPicFeatsData.sel_show_culture_groups[cul_idx])
      continue
    const now_node_radius =
      ((node_max_radius - node_min_radius) * cityPicFeatsData.city_closeness_centrality[i]) /
        max_r_val +
      node_min_radius
    const now_city_color = hsl_color_obj2str(cities_color_after_view.value[i])
    const node_id = `geo_city_node_${i}`
    inner_content += `<circle cx="${cities_x.value[i]}" cy="${cities_y.value[i]}" fill="${now_city_color}" r="${now_node_radius}" id=${node_id}></circle>`
    cities_show.push(i)
  }
  return {
    inner_content: inner_content,
    cities_show: cities_show
  }
}
function redraw_nodes_by_svg() {
  if (!if_map_loaded.value) return
  if (svgOverlay != undefined) map.removeLayer(svgOverlay)

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    reset_cities_client_pos()
  }
  const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svgElement.setAttribute('viewBox', `0 0 ${addded_svg_w} ${added_svg_h}`)

  const gen_svg_res = gen_geo_nodes_svg_elements()
  const inner_content = gen_svg_res.inner_content
  svgElement.innerHTML = inner_content
  var latLngBounds = L.latLngBounds([
    [90, 180],
    [-90, -180]
  ])
  // map.fitBounds(latLngBounds)

  svgOverlay = L.svgOverlay(svgElement, latLngBounds, {
    opacity: node_opacity,
    interactive: true
  }).addTo(map)
}
function gen_geo_cities_names_elements() {
  const cities_show = [] as number[]
  let inner_content = ''
  const max_r_val = Math.max(...cityPicFeatsData.city_closeness_centrality)
  for (let i = 0; i < cityPicFeatsData.cities_pos.length; i += 1) {
    if (cityPicFeatsData.now_show_status == 0 && !cityPicFeatsData.sel_show_cities[i]) continue
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[i]
    if (cityPicFeatsData.now_show_status == 1 && !cityPicFeatsData.sel_show_culture_groups[cul_idx])
      continue
    cities_show.push(i)
    const now_node_radius =
      ((node_max_radius - node_min_radius) * cityPicFeatsData.city_closeness_centrality[i]) /
        max_r_val +
      node_min_radius
    if (i != 27)
      inner_content += `<text x="${cities_x.value[i]}" y="${cities_y.value[i] - now_node_radius}" font-size="0.7" fill="#fff" text-anchor="middle">${cityPicFeatsData.cities_names[i]}</text>`
    else
      inner_content += `<text x="${cities_x.value[i]}" y="${cities_y.value[i] + now_node_radius + 0.6}" font-size="0.7" fill="#fff" text-anchor="middle">${cityPicFeatsData.cities_names[i]}</text>`
  }

  return {
    inner_content: inner_content,
    cities_show: cities_show
  }
}
function redraw_cities_names_by_svg() {
  if (!if_map_loaded.value) return
  if (svg_cities_names_overlay != undefined) map.removeLayer(svg_cities_names_overlay)

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    reset_cities_client_pos()
  }
  const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svgElement.setAttribute('viewBox', `0 0 ${addded_svg_w} ${added_svg_h}`)

  const gen_svg_res = gen_geo_cities_names_elements()
  const inner_content = gen_svg_res.inner_content
  svgElement.innerHTML = inner_content
  var latLngBounds = L.latLngBounds([
    [90, 180],
    [-90, -180]
  ])

  svg_cities_names_overlay = L.svgOverlay(svgElement, latLngBounds, {
    opacity: 1,
    interactive: true
  }).addTo(map)
}
// 为边与节点添加监听器 展示信息
function add_nodes_event_listener(cities_idx: number[]) {
  cities_idx.forEach((city_idx) => {
    const node_id = `geo_city_node_${city_idx}`
    const city_ele = document.getElementById(node_id) as HTMLElement
    city_ele.addEventListener('mouseenter', (e) => {
      handle_hover_node(e, city_idx)
    })
    city_ele.addEventListener('mouseout', handle_node_out)
  })
}
function add_edges_event_listener(edges: number[][]) {
  edges.forEach((cities_in_edge) => {
    const edge_id = `geo_edge_n${cities_in_edge[0]}_${cities_in_edge[1]}`
    const edge_ele = document.getElementById(edge_id) as HTMLElement
    edge_ele.addEventListener('mouseenter', (e) => {
      handle_hover_edge(e, cities_in_edge[0], cities_in_edge[1])
    })
    edge_ele.addEventListener('mouseout', handle_edge_out)
  })
}
// 整合上面的函数 将点 边 text画在一个svg内
function redraw_all_by_svg() {
  if (!if_map_loaded.value) return
  if (svgOverlay != undefined) map.removeLayer(svgOverlay)

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    reset_cities_client_pos()
  }
  const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svgElement.setAttribute('viewBox', `0 0 ${addded_svg_w} ${added_svg_h}`)

  const gen_edges_svg_res = gen_geo_edges_svg_elements()
  const gen_nodes_svg_res = gen_geo_nodes_svg_elements()
  const gen_nodes_names_svg_res = gen_geo_cities_names_elements()
  const inner_content =
    gen_edges_svg_res.inner_content +
    gen_nodes_svg_res.inner_content +
    gen_nodes_names_svg_res.inner_content
  svgElement.innerHTML = inner_content
  var latLngBounds = L.latLngBounds([
    [90, 180],
    [-90, -180]
  ])

  svgOverlay = L.svgOverlay(svgElement, latLngBounds, {
    opacity: node_opacity,
    interactive: true
  }).addTo(map)
  add_nodes_event_listener(gen_nodes_svg_res.cities_show)
  add_edges_event_listener(gen_edges_svg_res.edges_show)
}

watch(
  () => cities_color_after_view.value,
  () => {
    // redraw_edges_by_svg()
    // redraw_nodes_by_svg()
    // redraw_cities_names_by_svg()
    redraw_all_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.cities_pos,
  () => {
    // redraw_edges_by_svg()
    // redraw_nodes_by_svg()
    // redraw_cities_names_by_svg()
    redraw_all_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.sel_show_cities,
  () => {
    // redraw_edges_by_svg()
    // redraw_nodes_by_svg()
    // redraw_cities_names_by_svg()
    redraw_all_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.sel_show_culture_groups,
  () => {
    // redraw_edges_by_svg()
    // redraw_nodes_by_svg()
    // redraw_cities_names_by_svg()
    redraw_all_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.now_show_status,
  () => {
    // redraw_edges_by_svg()
    // redraw_nodes_by_svg()
    // redraw_cities_names_by_svg()
    redraw_all_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.cities_sim_threshold,
  () => {
    // redraw_edges_by_svg()
    // redraw_nodes_by_svg()
    // redraw_cities_names_by_svg()
    redraw_all_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.main_sel_show_view,
  () => {
    map.invalidateSize(true)
  }
)
onMounted(() => {
  map = L.map('map', {
    center: [51.505, -0.09],
    zoom: map_zoom_rate.value,
    attributionControl: false,
    zoomControl: false
  })

  const user_name = 'tfsyg9b2ce'
  const style_id = 'clzcew09b00a301qq68p16g52'
  const access_token =
    'pk.eyJ1IjoidGZzeWc5YjJjZSIsImEiOiJjbHZ5NXdycjAwM3czMnFwN2lmeHNwbGJhIn0._mBlTF1XETGKh8UAIdVClA'
  const style_url =
    `https://api.mapbox.com/styles/v1/${user_name}/${style_id}/tiles/512/{z}/{x}/{y}?access_token=` +
    access_token
  // 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  L.tileLayer(style_url, {}).addTo(map)

  map.addEventListener('zoomend', () => {
    map_zoom_rate.value = map.getZoom()
  })

  map.addEventListener('moveend', () => {})
  if_map_loaded.value = true
})

function reset_threshold(target_val: number) {
  cityPicFeatsData.cities_sim_threshold = target_val
}
</script>

<template>
  <div class="geo_network_box" id="geo_network_outer_box">
    <div class="geo_network_box_title">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
      >
        <defs>
          <linearGradient
            v-for="(grad_color_obj, grad_color_idx) in cities_grad_color"
            :key="grad_color_idx"
            :id="`city${grad_color_obj.city1}-city${grad_color_obj.city2}_grad_color`"
            :x1="grad_color_obj.x1 + '%'"
            :y1="grad_color_obj.y1 + '%'"
            :x2="grad_color_obj.x2 + '%'"
            :y2="grad_color_obj.y2 + '%'"
          >
            <stop :stop-color="grad_color_obj.c1" offset="0%"></stop>
            <stop :stop-color="grad_color_obj.c2" offset="100%"></stop>
          </linearGradient>
        </defs>

        <path
          d="M13.0769 7.4591C13.0769 7.18679 12.9136 7.00771 12.7216 6.89048L3.91725 1.49417C3.84617 1.4231 3.70494 1.4231 3.56186 1.4231C3.06525 1.4231 2.9231 1.77848 2.9231 2.06186V12.7843C2.9231 13.1388 3.06525 13.4231 3.56186 13.4231C3.70402 13.4231 3.77509 13.4231 3.91725 13.352L12.7216 8.02587C12.9136 7.9114 13.0769 7.68894 13.0769 7.4591Z"
          fill="#1A2134"
        />
      </svg>
      <span class="title_content"> Geographic Network </span>
      <div class="threshold_selection">
        <span class="selection_name">Threshold</span>
        <span class="selection_box">
          <span class="selected_one">
            <span> {{ cityPicFeatsData.cities_sim_threshold }} </span>
            <button>
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
            </button>
          </span>
          <div class="select_option_box">
            <div class="select_inner_option_box">
              <div class="select_option" @click="reset_threshold(0.01)">0.01</div>
              <div class="select_option" @click="reset_threshold(0.02)">0.02</div>
              <div class="select_option" @click="reset_threshold(0.04)">0.04</div>
            </div>
          </div>
        </span>
      </div>
    </div>
    <div class="geo_network_place">
      <div id="map"></div>
    </div>
    <div
      class="node_hover_assist_tooltip"
      v-show="now_hover_node >= 0"
      :tooltip="hover_node_tooltip_pos.tooltip"
      :style="{
        left: hover_node_tooltip_pos.x + 'px',
        top: hover_node_tooltip_pos.y + 'px'
      }"
    ></div>
    <div
      class="edge_hover_assist_tooltip"
      v-show="now_hover_edge[0] >= 0 && now_hover_edge[1] >= 0"
      :tooltip="hover_edge_tooltip_pos.tooltip"
      :style="{
        left: hover_edge_tooltip_pos.x + 'px',
        top: hover_edge_tooltip_pos.y + 'px'
      }"
    ></div>
  </div>
</template>

<style scoped>
.geo_network_box {
  width: 100%;
  height: 100%;
  background: #fff;
  position: relative;
}

.geo_network_box_title {
  width: 100%;
  /* height: 20px; */
  height: 30px;
  padding-bottom: 8px;

  display: flex;
  flex-direction: row;
  justify-content: left;
  align-items: center;
}

.geo_network_box_title > svg {
  width: 16px;
  height: 16px;
}
.geo_network_box_title > .title_content {
  color: var(--black, #1a2134);

  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;

  padding: 0 10px;
  width: calc(100% - 180px - 20px);
}

.geo_network_place {
  width: 100%;
  /* height: calc(100% - 28px); */
  height: calc(100% - 38px);
  border-radius: 4px;

  background-color: azure;
  overflow: hidden;
  position: relative;
}

.geo_network_place #map {
  width: 100%;
  height: 100%;
}

/* 展示节点信息 */
.node_hover_assist_tooltip,
.edge_hover_assist_tooltip {
  position: absolute;
  width: 0;
  height: 0;
  z-index: 999;
}
.node_hover_assist_tooltip::after {
  width: 100px;
}
.node_hover_assist_tooltip::after,
.node_hover_assist_tooltip::before,
.edge_hover_assist_tooltip::after,
.edge_hover_assist_tooltip::before {
  display: block;
}
/* edge信息 */
.edge_hover_assist_tooltip::after {
  width: 150px;
}
</style>
<style scoped>
.threshold_selection {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.threshold_selection > .selection_name {
  color: #1a2134;
  font-family: Inter;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  padding-right: 10px;
}
.threshold_selection > .selection_box {
  width: 87px;
  border-radius: 4px;
  border: 1px solid var(--gray, #dfe1e5);

  position: relative;
}
.threshold_selection > .selection_box > .selected_one {
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: calc(100% - 16px);
  height: 100%;
  padding: 4px 8px;
}
.threshold_selection > .selection_box > .selected_one > span {
  color: var(--black, #1a2134);

  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.threshold_selection > .selection_box > .selected_one > button {
  padding: 0;
  outline: 0;
  border: 0;
  margin: 0;
  background: none;

  width: 20px;
  height: 20px;
  flex-shrink: 0;
  cursor: pointer;
}
.threshold_selection > .selection_box > .selected_one > button > svg {
  width: 100%;
  height: 100%;
}
.threshold_selection > .selection_box > .select_option_box {
  position: absolute;
  width: 100%;
  top: 100%;
  padding-top: 5px;

  z-index: 999;
}
.threshold_selection > .selection_box > .select_option_box > .select_inner_option_box {
  width: 100%;

  border: 1px solid var(--gray, #dfe1e5);
  border-radius: 4px;
  overflow: hidden;
  background-color: #fff;
}
.threshold_selection > .selection_box > .select_option_box .select_option {
  width: calc(100% - 16px);
  padding: 4px 8px;

  color: var(--black, #1a2134);

  /* body_text */
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;

  cursor: pointer;
}
.threshold_selection > .selection_box > .select_option_box .select_option:hover {
  /* filter: brightness(0.8); */
  background-color: #dfe1e5;
}
.threshold_selection > .selection_box:not(:hover) .select_option_box {
  display: none;
}
</style>
