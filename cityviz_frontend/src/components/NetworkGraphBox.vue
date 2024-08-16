<script setup lang="ts">
import { useCityPicFeatStore } from '@/stores/cityPicFeat'
import { computed, ref } from 'vue'
const cityPicFeatsData = useCityPicFeatStore()

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
const max_edge_len = 10
function start_move(e: MouseEvent) {
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

function hsl_color_obj2str(color_obj: { h: number; s: number; l: number; a: number }) {
  if (color_obj == undefined) return `hsla(180, 100%, 100%, 0)`
  else return `hsla(${color_obj.h}, ${color_obj.s}%, ${color_obj.l}%, ${color_obj.a})`
}
function get_city_color(city_idx: number) {
  if (cityPicFeatsData.now_show_status == 0) {
    return hsl_color_obj2str(cityPicFeatsData.cities_colors[city_idx])
  } else {
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[city_idx]
    return hsl_color_obj2str(cityPicFeatsData.culture_groups_colors[cul_idx])
  }
}

function map_std_val2svg_pos(std_val: number) {
  return std_val * 100 + 200
}
const cities_node_pos = computed(() => {
  const res = [] as { pos: number[]; city_idx: number }[]
  cityPicFeatsData.cities_tsne_pos.forEach((city_node_pos, city_idx) => {
    if (cityPicFeatsData.now_show_status == 0 && !cityPicFeatsData.sel_show_cities[city_idx]) return
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[city_idx]
    if (cityPicFeatsData.now_show_status == 1 && !cityPicFeatsData.sel_show_culture_groups[cul_idx])
      return

    res.push({ pos: city_node_pos, city_idx: city_idx })
  })
  return res
})
const cities_edges = computed(() => {
  const res = [] as { start: number[]; end: number[]; sim: number; mid: number[]; w: number }[]
  const cities_num = cityPicFeatsData.cities_tsne_pos.length
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

      // 没被选中 可以正常显示
      const cities_sim =
        (cityPicFeatsData.normalized_cities_conf_matrix[c1_idx][c2_idx] +
          cityPicFeatsData.normalized_cities_conf_matrix[c2_idx][c1_idx]) /
        2
      if (cities_sim <= 0.05) continue
      const start_pos = cityPicFeatsData.cities_tsne_pos[c1_idx]
      const end_pos = cityPicFeatsData.cities_tsne_pos[c2_idx]
      const mid_pos = [(start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2]
      const w = max_edge_len * cities_sim
      res.push({
        start: [map_std_val2svg_pos(start_pos[0]), map_std_val2svg_pos(start_pos[1])],
        end: [map_std_val2svg_pos(end_pos[0]), map_std_val2svg_pos(end_pos[1])],
        mid: [map_std_val2svg_pos(mid_pos[0]), map_std_val2svg_pos(mid_pos[1])],
        sim: cities_sim,
        w: w
      })
    }
  }
  return res
})
</script>

<template>
  <div class="network_graph_main_content" @wheel="handle_wheel" @mousedown="start_move">
    <div class="zoom_box" :style="{ transform: `scale(${zoom_rate}%)` }">
      <div class="move_box" :style="{ left: box_pos[0] + 'px', top: box_pos[1] + 'px' }">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
          <line
            v-for="(edge_pos, edge_idx) in cities_edges"
            :key="edge_idx"
            :x1="edge_pos.start[0]"
            :x2="edge_pos.end[0]"
            :y1="edge_pos.start[1]"
            :y2="edge_pos.end[1]"
            stroke="#fff"
            :stroke-width="edge_pos.w"
          />
          <circle
            v-for="(city_tsne_pos_obj, city_idx) in cities_node_pos"
            :key="city_idx"
            :cx="map_std_val2svg_pos(city_tsne_pos_obj.pos[0])"
            :cy="map_std_val2svg_pos(city_tsne_pos_obj.pos[1])"
            r="3"
            stroke="#fff"
            stroke-width="1"
            :fill="get_city_color(city_tsne_pos_obj.city_idx)"
          />
          <text
            v-for="(city_tsne_pos_obj, city_idx) in cities_node_pos"
            :key="city_idx"
            :x="map_std_val2svg_pos(city_tsne_pos_obj.pos[0])"
            :y="map_std_val2svg_pos(city_tsne_pos_obj.pos[1]) - 5"
            font-size="3"
            fill="#fff"
            text-anchor="middle"
          >
            {{ cityPicFeatsData.cities_names[city_tsne_pos_obj.city_idx] }}
          </text>
        </svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
.network_graph_main_content {
  width: 100%;
  height: 100%;
  overflow: hidden;
  /* background: #fff; */
}
.network_graph_main_content .move_box svg {
  width: 400px;
  height: 400px;
  left: calc(50% - 200px);
  top: calc(50% - 200px);
  position: absolute;
}
.network_graph_main_content > .zoom_box {
  width: 100%;
  height: 100%;
  position: relative;
  transform-origin: center center;
}
.network_graph_main_content .move_box {
  width: 100%;
  height: 100%;
  position: absolute;
}
</style>
