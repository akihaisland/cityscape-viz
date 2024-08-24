<script setup lang="ts">
import { computed, defineProps, ref } from 'vue'
const bar_chart_data = defineProps({
  show_data: Array<number>,
  graph_title: String,
  bars_tag: Array<string>
})
const svg_size = ref({ w: 173, h: 106 })
const bar_horizontal_padding = 0.1
const now_bar_chart = ref(null as any as HTMLElement)

// 计算直方图的横轴跨度的
const bars_val = computed(() => {
  if (bar_chart_data.show_data != undefined) {
    return bar_chart_data.show_data
  }
  return [] as number[]
})

function num2format_str(num: number) {
  const decimalPlaces = 5
  // 将数字四舍五入到指定的小数位数
  let formattedNumber = num.toFixed(decimalPlaces)

  // 使用正则表达式去掉多余的 0 和小数点
  formattedNumber = formattedNumber.replace(/\.?0+$/, '')

  return formattedNumber
}
// x axis上的数值坐标
const data_range = computed(() => {
  if (bar_chart_data.show_data != undefined && bar_chart_data.show_data.length > 0) {
    return [Math.min(...bar_chart_data.show_data), Math.max(...bar_chart_data.show_data)]
  }
  return [0, 0]
})
const bars_num = computed(() => {
  let bars_num = 2
  if (bar_chart_data.show_data != undefined) bars_num += bar_chart_data.show_data.length
  return bars_num
})
const x_axis_data = computed(() => {
  const x_axis_len = svg_size.value.w - 16 - 30
  const per_bar_w = x_axis_len / bars_num.value / 1.2

  let now_pos = 30 + per_bar_w * (1 + bar_horizontal_padding * 3)
  const bars_pos = [] as number[][]
  for (let i = 0; i < bars_num.value - 2; i += 1) {
    bars_pos.push([now_pos, now_pos + per_bar_w])
    now_pos += per_bar_w * (bar_horizontal_padding * 2 + 1)
  }

  now_pos = 30 + per_bar_w * (1 + 0.5 + bar_horizontal_padding * 3)
  const bars_tag_pos = [] as number[]
  for (let i = 0; i < bars_num.value - 2; i += 1) {
    bars_tag_pos.push(now_pos)
    now_pos += per_bar_w * (bar_horizontal_padding * 2 + 1)
  }

  const bars_bounds_title = [] as string[]
  for (let i = 0; i < bars_num.value - 2; i += 1) {
    if (bar_chart_data.bars_tag != undefined) bars_bounds_title.push(bar_chart_data.bars_tag[i])
    else bars_bounds_title.push('')
  }
  return {
    start: 30,
    end: svg_size.value.w - 16,
    bars_pos: bars_pos,
    bars_tag_pos: bars_tag_pos,
    bars_bounds_title: bars_bounds_title,
    per_bar_w: per_bar_w
  }
})
const delta_y = computed(() => {
  let start_delta = 0.0001
  let nxt_multiply = 0 // x2 x2.5 x2, ...
  // let end_val = 10
  let raw_end = 0.002
  raw_end = data_range.value[0]

  // if (bar_chart_data.graph_title == 'Building Color')
  //   console.log('raw_data: ', raw_end, ', ', bar_chart_data.graph_title, bar_chart_data.show_data)

  // while (end_val > 6) {
  //   if (nxt_multiply == 0) {
  //     start_delta *= 2
  //     nxt_multiply = 1
  //   } else if (nxt_multiply == 1) {
  //     start_delta *= 2.5
  //     nxt_multiply = 2
  //   } else {
  //     start_delta *= 2
  //     nxt_multiply = 0
  //   }

  //   end_val = Math.ceil(raw_end / start_delta)
  // }
  let start_val = 0,
    end_val = 50
  while (end_val - start_val > 6) {
    if (nxt_multiply == 0) {
      start_delta *= 2
      nxt_multiply = 1
    } else if (nxt_multiply == 1) {
      start_delta *= 2.5
      nxt_multiply = 2
    } else {
      start_delta *= 2
      nxt_multiply = 0
    }

    start_val = Math.floor(data_range.value[0] / start_delta)
    end_val = Math.ceil(data_range.value[1] / start_delta)
  }
  return start_delta
})

const y_axis_data = computed(() => {
  let raw_end = 0.002
  if (bar_chart_data.show_data != undefined) raw_end = Math.max(...bar_chart_data.show_data)

  const start_val = Math.floor(data_range.value[0] / delta_y.value)
  const end_val = Math.ceil(data_range.value[1] / delta_y.value)
  let bars_num = end_val - start_val
  // if (histgram_data_range.value.num == 0) {
  //   bars_num = 1
  // }
  const per_bar_h = (svg_size.value.h - 20 - 15) / (bars_num + 0.5)
  const bars_t_pos = [svg_size.value.h - 20] as number[]
  const axis_start_val = Math.floor(data_range.value[0] / delta_y.value) * delta_y.value
  const bars_t_title = [num2format_str(axis_start_val)] as string[]
  for (let i = 1; i <= bars_num; i++) {
    bars_t_pos.push(bars_t_pos[0] - i * per_bar_h)
    bars_t_title.push(num2format_str(axis_start_val + i * delta_y.value))
  }
  return {
    start: svg_size.value.h - 20,
    end: 15,
    full_height: svg_size.value.h - 20 - 15,
    bars_pos: bars_t_pos,
    bars_bounds_title: bars_t_title,
    per_bar_h: per_bar_h,
    start_val: start_val * delta_y.value,
    end_val: end_val * delta_y.value
  }
})
const histgram_bars_pos = computed(() => {
  const bars_pos = [] as number[][]
  const per_bar_h = y_axis_data.value.per_bar_h
  const per_bar_w = x_axis_data.value.per_bar_w
  const start_pos = [
    x_axis_data.value.start + per_bar_w * (1 + 3 * bar_horizontal_padding),
    y_axis_data.value.start
  ]

  let bars_path_pos = `M${start_pos[0]},${start_pos[1]}`
  let now_pos = start_pos as number[]

  bars_val.value.forEach((bar_val, bar_idx) => {
    const new_y =
      start_pos[1] - ((bar_val - y_axis_data.value.start_val) * per_bar_h) / delta_y.value
    bars_path_pos += ` L${now_pos[0]},${new_y} L${now_pos[0] + per_bar_w},${new_y} L${now_pos[0] + per_bar_w},${start_pos[1]}`
    now_pos = [start_pos[0] + (bar_idx + 1) * per_bar_w * (1 + 2 * bar_horizontal_padding), new_y]
    bars_pos.push(now_pos)
    bars_path_pos += ` L${now_pos[0]},${start_pos[1]}`
  })
  bars_path_pos += ` Z`

  return bars_path_pos
})

// 展示数据
const now_hover_bar = ref(-1)
let now_hover_timer = -1
let now_hover_pos = [-1, -1]
const hover_bar_tooltip_pos = computed(() => {
  if (
    now_hover_bar.value >= 0 &&
    bar_chart_data.show_data != undefined &&
    bar_chart_data.show_data.length > 0 &&
    bar_chart_data.bars_tag != undefined
  ) {
    const now_tooltip =
      bar_chart_data.bars_tag[now_hover_bar.value] +
      `\nValue: ${bar_chart_data.show_data[now_hover_bar.value].toFixed(5)}`
    return {
      x: now_hover_pos[0],
      y: now_hover_pos[1],
      tooltip: now_tooltip
    }
  }
  return { x: now_hover_pos[0], y: now_hover_pos[1], tooltip: '' }
})
function handle_hover_bar(e: MouseEvent, data_show_idx: number) {
  if (now_hover_timer) clearTimeout(now_hover_timer)
  now_hover_timer = setTimeout(() => {
    now_hover_bar.value = data_show_idx
    // console.log(e)

    now_hover_pos = [e.offsetX, e.offsetY]
  }, 200)
}
function handle_bar_out() {
  if (now_hover_timer) clearTimeout(now_hover_timer)
  now_hover_bar.value = -1
}
</script>

<template>
  <div class="histgram_chart_box" ref="now_bar_chart">
    <svg xmlns="http://www.w3.org/2000/svg" :viewBox="`0 0 ${svg_size.w} ${svg_size.h}`">
      <path
        :d="`M35,5 L5,5 L5,${svg_size.h - 5} L${svg_size.w - 5},${svg_size.h - 5} L${svg_size.w - 5},5 L${svg_size.w - 35},5`"
        stroke-width="1"
        stroke="#C8C8C8"
        fill="none"
      />
      <!-- title -->
      <text
        :x="`${svg_size.w / 2}`"
        :y="`${10}`"
        font-family="Arial"
        font-size="12"
        text-anchor="middle"
      >
        {{ bar_chart_data.graph_title }}
      </text>
      <!-- y assist -->
      <path
        v-for="(bar_y_pos, y_idx) in y_axis_data.bars_pos"
        :key="y_idx"
        :d="`M${x_axis_data.start},${bar_y_pos} L${x_axis_data.end},${bar_y_pos}`"
        stroke="#C8C8C8"
        stroke-width="1"
      />
      <!-- bars -->
      <path :d="histgram_bars_pos" stroke="none" fill="url(#histMyGradient)" />
      <!-- x axis -->
      <path
        :d="`M${x_axis_data.start}, ${y_axis_data.start} L ${x_axis_data.end},${y_axis_data.start}`"
        stroke="#000"
        stroke-width="1"
      />
      <!-- <text
        v-for="(bar_x_pos, x_idx) in x_axis_data.bars_tag_pos"
        :key="x_idx"
        :x="`${bar_x_pos}`"
        :y="`${y_axis_data.start + 12}`"
        font-family="Arial"
        font-size="8"
        text-anchor="middle"
      >
        {{ x_axis_data.bars_bounds_title[x_idx] }}
      </text> -->
      <!-- y axis -->
      <path
        :d="`M${x_axis_data.start}, ${y_axis_data.start} L ${x_axis_data.start},${y_axis_data.end}`"
        stroke="#000"
        stroke-width="1"
      />
      <path
        :d="`M${x_axis_data.start}, ${y_axis_data.start} L${x_axis_data.start - 5}, ${y_axis_data.start}`"
        stroke="#000"
        stroke-width="1"
      />
      <path
        :d="`M${x_axis_data.start}, ${y_axis_data.end} L${x_axis_data.start - 5}, ${y_axis_data.end}`"
        stroke="#000"
        stroke-width="1"
      />
      <path
        v-for="(bar_y_pos, y_idx) in y_axis_data.bars_pos"
        :key="y_idx"
        :d="`M${x_axis_data.start},${bar_y_pos} L${x_axis_data.start - 5},${bar_y_pos}`"
        stroke="#000"
        stroke-width="1"
      />
      <rect
        v-for="(bar_x_pos, bar_idx) in x_axis_data.bars_pos"
        :key="bar_idx"
        :x="bar_x_pos[0]"
        :y="y_axis_data.end"
        :width="x_axis_data.per_bar_w"
        :height="y_axis_data.full_height"
        fill="transparent"
        @mouseenter="handle_hover_bar($event, bar_idx)"
        @mouseout="handle_bar_out"
      />
      <text
        v-for="(bar_y_pos, y_idx) in y_axis_data.bars_pos"
        :key="y_idx"
        :x="`${x_axis_data.start - 6}`"
        :y="`${bar_y_pos - 4 + 6}`"
        font-family="Arial"
        font-size="8"
        text-anchor="end"
      >
        {{ y_axis_data.bars_bounds_title[y_idx] }}
      </text>
    </svg>
    <div
      class="bar_tooltip_assist"
      v-show="now_hover_bar >= 0"
      :tooltip="hover_bar_tooltip_pos.tooltip"
      :style="{
        position: 'absolute',
        left: hover_bar_tooltip_pos.x + 'px',
        top: hover_bar_tooltip_pos.y + 'px',
        width: '0px',
        height: '0px',
        borderRadius: '50%'
      }"
    ></div>
  </div>
</template>

<style scoped>
.histgram_chart_box {
  width: 100%;
  height: 100%;
  position: relative;
}
.histgram_chart_box svg {
  width: 100%;
  height: 100%;
}
.histgram_chart_box svg text {
  user-select: none;
}

/* 展示节点信息 */
.bar_tooltip_assist {
  position: absolute;
}
.bar_tooltip_assist::after {
  width: 100px;
}
.bar_tooltip_assist::after,
.bar_tooltip_assist::before {
  display: block;
}
</style>
