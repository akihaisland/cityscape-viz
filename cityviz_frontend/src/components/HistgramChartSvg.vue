<script setup lang="ts">
import { computed, defineProps, ref } from 'vue'
const histgram_data = defineProps({
  show_data: Array<number>,
  graph_title: String
})
const svg_size = ref({ w: 173, h: 106 })

// 计算直方图的横轴跨度的
const histgram_data_range = computed(() => {
  if (histgram_data.show_data != undefined && histgram_data.show_data.length > 0)
    return {
      min: Math.min(...histgram_data.show_data),
      max: Math.max(...histgram_data.show_data),
      num: histgram_data.show_data.length
    }
  else return { min: 0, max: 0, num: 0 }
})
const delta_x = computed(() => {
  let start_delta = 0.0001
  let nxt_multiply = 0 // x5 x2 x5, ...
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

    start_val = Math.floor(histgram_data_range.value.min / start_delta)
    end_val = Math.ceil(histgram_data_range.value.max / start_delta)
  }
  return start_delta
})
const bars_val = computed(() => {
  const bar_per_w = delta_x.value / 5
  const bars_lower_bound = Math.floor(histgram_data_range.value.min / delta_x.value) * delta_x.value
  const bars_upper_bounds = [] as number[]
  let bars_upper_bound = bars_lower_bound
  const num_in_bars = [] as number[] // 每个bar里面的元素数量
  while (
    bars_upper_bound < histgram_data_range.value.max ||
    bars_upper_bounds.length % 5 != 0 ||
    bars_upper_bounds.length == 0
  ) {
    bars_upper_bound += bar_per_w
    bars_upper_bounds.push(bars_upper_bound)
    num_in_bars.push(0)
  }

  // 便利入桶
  if (histgram_data.show_data == undefined) return num_in_bars
  histgram_data.show_data.forEach((now_val) => {
    for (let i = 0; i < bars_upper_bounds.length; i += 1) {
      if (now_val < bars_upper_bounds[i]) {
        num_in_bars[i] += 1
        break
      }
    }
  })
  return num_in_bars
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
const x_axis_data = computed(() => {
  const bar_per_w = delta_x.value / 5
  const bars_lower_bound = Math.floor(histgram_data_range.value.min / delta_x.value) * delta_x.value
  const bars_bounds = [bars_lower_bound] as number[]
  let bars_upper_bound = bars_lower_bound
  let bar_num = 0
  while (
    bars_upper_bound < histgram_data_range.value.max ||
    (bars_bounds.length - 1) % 5 != 0 ||
    bar_num == 0
  ) {
    bars_upper_bound += bar_per_w

    bars_bounds.push(bars_upper_bound)
    bar_num += 1
  }
  bar_num /= 5
  const x_axis_len = svg_size.value.w - 16 - 30
  const per_bar_w = x_axis_len / (bar_num + 1)
  let now_pos = 30 + per_bar_w / 2
  const bars_pos = [now_pos]
  for (let i = 0; i < bar_num; i += 1) {
    now_pos += per_bar_w
    bars_pos.push(now_pos)
  }

  const bars_bounds_title = [] as string[]
  for (let i = 0; i < bars_bounds.length; i += 5) {
    bars_bounds_title.push(num2format_str(bars_bounds[i]))
  }
  return {
    start: 30,
    end: svg_size.value.w - 16,
    bars_pos: bars_pos,
    bars_bounds_title: bars_bounds_title,
    per_bar_w: per_bar_w
  }
})
const delta_y = computed(() => {
  let start_delta = 0.0001
  let nxt_multiply = 0 // x2 x2.5 x2, ...
  let end_val = 10
  let raw_end = Math.max(...bars_val.value) / histgram_data_range.value.num

  if (histgram_data_range.value.num == 0) raw_end = 0
  while (end_val > 6) {
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

    end_val = Math.ceil(raw_end / start_delta)
  }
  return start_delta
})
const y_axis_data = computed(() => {
  let bars_num = Math.ceil(
    Math.max(...bars_val.value) / histgram_data_range.value.num / delta_y.value
  )
  if (histgram_data_range.value.num == 0) {
    bars_num = 1
  }
  const per_bar_h = (svg_size.value.h - 20 - 15) / (bars_num + 0.5)
  const bars_t_pos = [svg_size.value.h - 20] as number[]
  const bars_t_title = ['0'] as string[]
  for (let i = 1; i <= bars_num; i++) {
    bars_t_pos.push(bars_t_pos[0] - i * per_bar_h)
    bars_t_title.push(num2format_str(i * delta_y.value))
  }
  return {
    start: svg_size.value.h - 20,
    end: 15,
    bars_pos: bars_t_pos,
    bars_bounds_title: bars_t_title,
    per_bar_h: per_bar_h
  }
})
const histgram_bars_pos = computed(() => {
  const bars_pos = [] as number[][]
  const per_bar_h = y_axis_data.value.per_bar_h
  const per_bar_w = x_axis_data.value.per_bar_w
  const start_pos = [x_axis_data.value.start + per_bar_w / 2, y_axis_data.value.start]

  let bars_path_pos = `M${start_pos[0]},${start_pos[1]}`
  let now_pos = start_pos as number[]

  bars_val.value.forEach((bar_num, bar_idx) => {
    let bar_h_val = bar_num / histgram_data_range.value.num
    if (histgram_data_range.value.num == 0) bar_h_val = 0
    const new_y = start_pos[1] - (bar_h_val * per_bar_h) / delta_y.value
    bars_path_pos += ` L${now_pos[0]},${new_y}`
    now_pos = [start_pos[0] + ((bar_idx + 1) * per_bar_w) / 5, new_y]
    bars_pos.push(now_pos)
    bars_path_pos += ` L${now_pos[0]},${now_pos[1]}`
  })
  bars_path_pos += ` L${now_pos[0]},${start_pos[1]} L${start_pos[0]},${start_pos[1]} Z`

  return bars_path_pos
})
</script>

<template>
  <div class="histgram_chart_box">
    <svg xmlns="http://www.w3.org/2000/svg" :viewBox="`0 0 ${svg_size.w} ${svg_size.h}`">
      <!-- <defs>
        <linearGradient id="histMyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color: #2d87aa; stop-opacity: 1" />
          <stop offset="100%" style="stop-color: #18263a; stop-opacity: 1" />
        </linearGradient>
      </defs> -->
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
        {{ histgram_data.graph_title }}
      </text>
      <!-- y assist -->
      <path
        v-for="(bar_y_pos, y_idx) in y_axis_data.bars_pos"
        :key="y_idx"
        :d="`M${x_axis_data.start},${bar_y_pos} L${x_axis_data.end},${bar_y_pos}`"
        stroke="#C8C8C8"
        stroke-width="1"
      />
      <!-- histgram bars -->
      <path :d="histgram_bars_pos" stroke="none" fill="url(#histMyGradient)" />
      <!-- x axis -->
      <path
        :d="`M${x_axis_data.start}, ${y_axis_data.start} L ${x_axis_data.end},${y_axis_data.start}`"
        stroke="#000"
        stroke-width="1"
      />
      <path
        :d="`M${x_axis_data.start}, ${y_axis_data.start} L${x_axis_data.start}, ${y_axis_data.start + 5}`"
        stroke="#000"
        stroke-width="1"
      />
      <path
        :d="`M${x_axis_data.end}, ${y_axis_data.start} L${x_axis_data.end}, ${y_axis_data.start + 5}`"
        stroke="#000"
        stroke-width="1"
      />
      <path
        v-for="(bar_x_pos, x_idx) in x_axis_data.bars_pos"
        :key="x_idx"
        :d="`M${bar_x_pos}, ${y_axis_data.start} L${bar_x_pos}, ${y_axis_data.start + 5}`"
        stroke="#000"
        stroke-width="1"
      />
      <text
        v-for="(bar_x_pos, x_idx) in x_axis_data.bars_pos"
        :key="x_idx"
        :x="`${bar_x_pos}`"
        :y="`${y_axis_data.start + 12}`"
        font-family="Arial"
        font-size="8"
        text-anchor="middle"
      >
        {{ x_axis_data.bars_bounds_title[x_idx] }}
      </text>
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
  </div>
</template>

<style scoped>
.histgram_chart_box {
  width: 100%;
  height: 100%;
}
.histgram_chart_box svg {
  width: 100%;
  height: 100%;
}
.histgram_chart_box svg text {
  user-select: none;
}
</style>
