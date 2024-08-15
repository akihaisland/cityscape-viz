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

let svgOverlay: L.SVGOverlay
let svg_edges_overlay: L.SVGOverlay
let svg_cities_names_overlay: L.SVGOverlay
let addded_svg_w = 400
let added_svg_h = 400
const edge_max_w = 5
const node_max_radius = 2
const cities_sim_threshold = 0.05
const line_opacity = 0.7

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
function redraw_edges_by_svg() {
  if (!if_map_loaded.value) return
  if (svg_edges_overlay != undefined) map.removeLayer(svg_edges_overlay)

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    reset_cities_client_pos()
  }

  const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svgElement.setAttribute('viewBox', `0 0 ${addded_svg_w} ${added_svg_h}`)
  const cities_num = cities_x.value.length

  let inner_content = ''
  for (let c1_idx = 0; c1_idx < cities_num; c1_idx += 1) {
    for (let c2_idx = 0; c2_idx < cities_num; c2_idx += 1) {
      if (c1_idx <= c2_idx) continue
      if (
        cityPicFeatsData.now_show_status == 0 &&
        (!cityPicFeatsData.sel_show_cities[c1_idx] || !cityPicFeatsData.sel_show_cities[c2_idx])
      )
        continue
      const cul1_idx = cityPicFeatsData.cities2cul_group_idx[c1_idx]
      const cul2_idx = cityPicFeatsData.cities2cul_group_idx[c1_idx]
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
      const now_edge_w = cities_sim * edge_max_w
      if (cities_sim > cities_sim_threshold)
        inner_content += `<path d="${now_path_d}" stroke="${stroke_color}" stroke-width="${now_edge_w}" fill="none" />`
    }
  }

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
function redraw_nodes_by_svg() {
  if (!if_map_loaded.value) return
  if (svgOverlay != undefined) map.removeLayer(svgOverlay)

  if (cities_x.value.length == 0 || cities_y.value.length == 0) {
    reset_cities_client_pos()
  }
  const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svgElement.setAttribute('viewBox', `0 0 ${addded_svg_w} ${added_svg_h}`)
  const max_r_val = Math.max(...cityPicFeatsData.city_closeness_centrality)
  let inner_content = ''
  for (let i = 0; i < cityPicFeatsData.cities_pos.length; i += 1) {
    if (cityPicFeatsData.now_show_status == 0 && !cityPicFeatsData.sel_show_cities[i]) continue
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[i]
    if (cityPicFeatsData.now_show_status == 1 && !cityPicFeatsData.sel_show_culture_groups[cul_idx])
      continue
    const now_node_radius =
      (node_max_radius * cityPicFeatsData.city_closeness_centrality[i]) / max_r_val
    const now_city_color = hsl_color_obj2str(cities_color_after_view.value[i])
    inner_content += `<circle cx="${cities_x.value[i]}" cy="${cities_y.value[i]}" fill="${now_city_color}" r="${now_node_radius}"></circle>`
  }
  svgElement.innerHTML = inner_content
  var latLngBounds = L.latLngBounds([
    [90, 180],
    [-90, -180]
  ])
  // map.fitBounds(latLngBounds)

  svgOverlay = L.svgOverlay(svgElement, latLngBounds, {
    opacity: 1,
    interactive: true
  }).addTo(map)
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
  let inner_content = ''
  const max_r_val = Math.max(...cityPicFeatsData.city_closeness_centrality)
  for (let i = 0; i < cityPicFeatsData.cities_pos.length; i += 1) {
    const now_node_radius =
      (node_max_radius * cityPicFeatsData.city_closeness_centrality[i]) / max_r_val
    if (i != 27)
      inner_content += `<text x="${cities_x.value[i]}" y="${cities_y.value[i] - now_node_radius}" font-size="0.7" fill="#fff" text-anchor="middle">${cityPicFeatsData.cities_names[i]}</text>`
    else
      inner_content += `<text x="${cities_x.value[i]}" y="${cities_y.value[i] + now_node_radius + 0.6}" font-size="0.7" fill="#fff" text-anchor="middle">${cityPicFeatsData.cities_names[i]}</text>`
  }

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

watch(
  () => cities_color_after_view.value,
  () => {
    redraw_edges_by_svg()
    redraw_nodes_by_svg()
    redraw_cities_names_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.cities_pos,
  () => {
    redraw_edges_by_svg()
    redraw_nodes_by_svg()
    redraw_cities_names_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.sel_show_cities,
  () => {
    redraw_edges_by_svg()
    redraw_nodes_by_svg()
    redraw_cities_names_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.sel_show_culture_groups,
  () => {
    redraw_edges_by_svg()
    redraw_nodes_by_svg()
    redraw_cities_names_by_svg()
  },
  { deep: true }
)
watch(
  () => cityPicFeatsData.now_show_status,
  () => {
    redraw_edges_by_svg()
    redraw_nodes_by_svg()
    redraw_cities_names_by_svg()
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
</script>

<template>
  <div class="geo_network_box">
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
      <span class="title_content"> Geographic network visualization </span>
    </div>
    <div class="geo_network_place">
      <div id="map"></div>
    </div>
  </div>
</template>

<style scoped>
.geo_network_box {
  width: 100%;
  height: 100%;
  background: #fff;
}

.geo_network_box_title {
  width: 100%;
  height: 20px;
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
}

.geo_network_place {
  width: 100%;
  height: calc(100% - 28px);
  border-radius: 4px;

  background-color: azure;
  overflow: hidden;
}

.geo_network_place #map {
  width: 100%;
  height: 100%;
}
</style>
