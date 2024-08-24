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
const node_max_r = 5
const node_min_r = 1
const node_opacity = 0.9
const cities_node_pos = computed(() => {
  const res = [] as { pos: number[]; city_idx: number; r: number; tooltip: string }[]
  const max_r_val = Math.max(...cityPicFeatsData.city_closeness_centrality)
  cityPicFeatsData.cities_tsne_pos.forEach((city_node_pos, city_idx) => {
    if (cityPicFeatsData.now_show_status == 0 && !cityPicFeatsData.sel_show_cities[city_idx]) return
    const cul_idx = cityPicFeatsData.cities2cul_group_idx[city_idx]
    if (cityPicFeatsData.now_show_status == 1 && !cityPicFeatsData.sel_show_culture_groups[cul_idx])
      return

    // 获取城市中心度
    const now_city_val =
      (cityPicFeatsData.city_closeness_centrality[city_idx] / max_r_val) *
        (node_max_r - node_min_r) +
      node_min_r
    let now_tooltip_content = `City: ${cityPicFeatsData.cities_names[city_idx]}\nDegree Centrality: ${cityPicFeatsData.city_closeness_centrality[city_idx]}`
    if (cityPicFeatsData.now_show_status == 1) {
      now_tooltip_content = `Culture Group: ${cityPicFeatsData.culture_groups_names[cul_idx]}\nDegree Centrality: ${cityPicFeatsData.city_closeness_centrality[city_idx]}`
    }
    res.push({
      pos: city_node_pos,
      city_idx: city_idx,
      r: now_city_val,
      tooltip: now_tooltip_content
    })
  })
  return res
})
const cities_edges = computed(() => {
  const res = [] as {
    start: number[]
    end: number[]
    sim: number
    mid: number[]
    w: number
    c1: number
    c2: number
  }[]
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
        w: w,
        c1: c1_idx,
        c2: c2_idx
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
    const node_obj = cities_node_pos.value[now_hover_node.value]
    const father_ele = document.getElementById('network_graph_view_box') as HTMLElement
    const father_pos_rect = father_ele.getBoundingClientRect()
    return {
      x: now_hover_pos[0] - father_pos_rect.left,
      y: now_hover_pos[1] - father_pos_rect.top,
      tooltip: node_obj.tooltip
    }
  }
  return { x: -1, y: -1, tooltip: '' }
})
function handle_hover_node(e: MouseEvent, data_show_idx: number) {
  if (node_hover_timer) clearTimeout(node_hover_timer)
  node_hover_timer = setTimeout(() => {
    now_hover_node.value = data_show_idx
    now_hover_pos = [e.clientX, e.clientY]
  }, 200)
}
function handle_node_out() {
  if (node_hover_timer) clearTimeout(node_hover_timer)
  now_hover_node.value = -1
}
function node_stroke_color(node_idx: number) {
  if (now_hover_node.value == -1) return '#fff'
  else if (node_idx == now_hover_node.value) return '#fff'
  else return '#ffffffa0'
}
// edge数据
const now_hover_edge = ref(-1)
let edge_hover_timer = -1
const hover_edge_tooltip_pos = computed(() => {
  if (now_hover_edge.value >= 0) {
    const edge_obj = cities_edges.value[now_hover_edge.value]
    const father_ele = document.getElementById('network_graph_view_box') as HTMLElement
    const father_pos_rect = father_ele.getBoundingClientRect()

    const edge_tooltip =
      `City: ${cityPicFeatsData.cities_names[edge_obj.c1]}, ${cityPicFeatsData.cities_names[edge_obj.c2]}\n` +
      `Similarity: ${edge_obj.sim.toFixed(5)}`
    return {
      x: now_hover_pos[0] - father_pos_rect.left,
      y: now_hover_pos[1] - father_pos_rect.top,
      tooltip: edge_tooltip
    }
  }
  return { x: -1, y: -1, tooltip: '' }
})
function handle_hover_edge(e: MouseEvent, data_show_idx: number) {
  if (edge_hover_timer) clearTimeout(edge_hover_timer)
  edge_hover_timer = setTimeout(() => {
    now_hover_edge.value = data_show_idx
    now_hover_pos = [e.clientX, e.clientY]
  }, 200)
}
function handle_edge_out() {
  if (edge_hover_timer) clearTimeout(edge_hover_timer)
  now_hover_edge.value = -1
}
function edge_stroke_color(edge_idx: number) {
  if (edge_idx == now_hover_edge.value) return '#fff'
  else return '#ffffffa0'
}
</script>

<template>
  <div
    class="network_graph_main_content"
    @wheel="handle_wheel"
    @mousedown="start_move"
    id="network_graph_view_box"
  >
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
            :stroke="edge_stroke_color(edge_idx)"
            :stroke-width="edge_pos.w"
            @mouseenter="handle_hover_edge($event, edge_idx)"
            @mouseout="handle_edge_out"
          />
          <circle
            v-for="(city_tsne_pos_obj, city_idx) in cities_node_pos"
            :key="city_idx"
            :cx="map_std_val2svg_pos(city_tsne_pos_obj.pos[0])"
            :cy="map_std_val2svg_pos(city_tsne_pos_obj.pos[1])"
            :r="city_tsne_pos_obj.r"
            :stroke="node_stroke_color(city_idx)"
            stroke-width="1"
            :fill="get_city_color(city_tsne_pos_obj.city_idx)"
            @mouseenter="handle_hover_node($event, city_idx)"
            @mouseout="handle_node_out"
            :style="{ opacity: node_opacity }"
          />
          <text
            v-for="(city_tsne_pos_obj, city_idx) in cities_node_pos"
            :key="city_idx"
            :x="map_std_val2svg_pos(city_tsne_pos_obj.pos[0])"
            :y="map_std_val2svg_pos(city_tsne_pos_obj.pos[1]) - cities_node_pos[city_idx].r - 2"
            font-size="3"
            :fill="node_stroke_color(city_idx)"
            text-anchor="middle"
          >
            {{ cityPicFeatsData.cities_names[city_tsne_pos_obj.city_idx] }}
          </text>
        </svg>
      </div>
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
      v-show="now_hover_edge >= 0"
      :tooltip="hover_edge_tooltip_pos.tooltip"
      :style="{
        left: hover_edge_tooltip_pos.x + 'px',
        top: hover_edge_tooltip_pos.y + 'px'
      }"
    ></div>
  </div>
</template>

<style scoped>
.network_graph_main_content {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
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

/* 展示节点信息 */
.node_hover_assist_tooltip,
.edge_hover_assist_tooltip {
  position: absolute;
  width: 0;
  height: 0;
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
