import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

interface HslaColor {
  h: number
  s: number
  l: number
  a: number
}

const backend_url = 'http://10.7.168.50:5050'

export const useCityPicFeatStore = defineStore('cityPicFeat', () => {
  // tsne降维后的坐标以及各种信息
  const tsne_pos = ref([] as number[][])
  const street_scales = ref([] as number[])
  const building_colors = ref([] as number[])
  const facade_material = ref([] as number[])
  const architectural_style = ref([] as number[])
  const greenery = ref([] as number[])
  const urban_sign = ref([] as number[])
  const idx2city_idxs = ref([] as number[])
  const idx2culture_group_idxs = ref([] as number[])
  const cities_names = ref([] as string[])
  const culture_groups_names = ref([] as string[])
  const cities_in_culture_groups = ref([] as number[][])
  const now_show_status = ref(0) // 保存当前展示的类型？0城市/ 1文化圈
  const sel_show_cities = ref([] as boolean[])
  const sel_show_culture_groups = ref([] as boolean[])
  const sel_show_nodes = ref([] as boolean[])
  // 混淆矩阵数据
  const normalized_cities_conf_matrix = ref([] as number[][])
  const normalized_cul_groups_conf_matrix = ref([] as number[][])
  // 城市的位置
  const cities_pos = ref([] as { lon: number; lat: number }[])
  const cities_tsne_pos = ref([] as number[][])
  // 颜色
  const cities_colors = ref([] as HslaColor[])
  const culture_groups_colors = ref([] as HslaColor[])
  // cul_group_status // 多种cul group的呈现形式
  const cul_group_status = ref(0)

  async function init_all_feats() {
    const test_num = 30000
    // 请求tsne降维的数据
    const req_tsne_res = (await axios.get(backend_url + '/api/tsneVec', {
      params: { vec_len: test_num }
    })) as { data: number[][] }
    tsne_pos.value = req_tsne_res.data

    // 请求streetScale的数据
    const street_scales_req_res = (await axios.get(backend_url + '/api/streetScale', {
      params: { vec_len: test_num }
    })) as { data: number[] }
    street_scales.value = street_scales_req_res.data

    // 请求greenery的数据
    const req_greenery_res = (await axios.get(backend_url + '/api/greenery', {
      params: { vec_len: test_num }
    })) as { data: number[] }
    greenery.value = req_greenery_res.data

    // data missing

    // 请求城市的数据
    const req_in_cities_res = (await axios.get(backend_url + '/api/data_cities', {
      params: { vec_len: test_num }
    })) as {
      data: {
        idx2city: number[]
        idx2culture_group: number[]
        cities_in_culture_groups: number[][]
        cities_name: string[]
        culture_groups_names: string[]
      }
    }
    idx2city_idxs.value = req_in_cities_res.data.idx2city
    idx2culture_group_idxs.value = req_in_cities_res.data.idx2culture_group
    cities_names.value = req_in_cities_res.data.cities_name
    const cul_names = req_in_cities_res.data.culture_groups_names
    culture_groups_names.value = cul_names
    cities_in_culture_groups.value = req_in_cities_res.data.cities_in_culture_groups

    // 设置所有节点为被选中状态
    let sel_show_nodes_value = [] as boolean[]
    tsne_pos.value.forEach(() => {
      sel_show_nodes_value.push(true)
    })
    sel_show_nodes.value = sel_show_nodes_value
    // 设置所有城市为被选中状态
    sel_show_nodes_value = [] as boolean[]
    cities_names.value.forEach(() => {
      sel_show_nodes_value.push(true)
    })
    sel_show_cities.value = sel_show_nodes_value
    // 设置所有城市为被选中状态
    sel_show_nodes_value = [] as boolean[]
    culture_groups_names.value.forEach(() => {
      sel_show_nodes_value.push(true)
    })
    sel_show_culture_groups.value = sel_show_nodes_value

    // 请求混淆矩阵的数据
    const req_conf_matrix_res = (await axios.get(backend_url + '/api/normalized_conf_matrix', {
      params: {}
    })) as { data: { city: number[][]; cul_group: number[][] } }
    normalized_cities_conf_matrix.value = req_conf_matrix_res.data.city
    normalized_cul_groups_conf_matrix.value = req_conf_matrix_res.data.cul_group

    // 请求城市位置的数据
    const req_cities_pos_res = (await axios.get(backend_url + '/api/cities_pos', {
      params: {}
    })) as { data: { lon: string; lat: string }[] }
    const tmp_cities_pos = [] as { lat: number; lon: number }[]
    req_cities_pos_res.data.forEach((raw_city_pos) => {
      tmp_cities_pos.push({ lon: Number(raw_city_pos.lon), lat: Number(raw_city_pos.lat) })
    })
    cities_pos.value = tmp_cities_pos

    // 请求城市tsne位置的数据
    const req_cities_tsne_pos_res = (await axios.get(backend_url + '/api/cities_tsne_pos', {
      params: {}
    })) as { data: number[][] }
    cities_tsne_pos.value = req_cities_tsne_pos_res.data

    // 请求配色数据
    const req_colors_res = (await axios.get(backend_url + '/api/colors', {
      params: {}
    })) as { data: { cities_colors: HslaColor[]; cul_groups_colors: HslaColor[] } }
    cities_colors.value = req_colors_res.data.cities_colors
    culture_groups_colors.value = req_colors_res.data.cul_groups_colors
  }

  const tsne_range = computed(() => {
    let mini_x = 10000
    let max_x = -10000
    let mini_y = 10000
    let max_y = -10000
    tsne_pos.value.forEach((now_pos) => {
      if (now_pos[0] > max_x) max_x = now_pos[0]
      if (now_pos[0] < mini_x) mini_x = now_pos[0]
      if (now_pos[1] > max_y) max_y = now_pos[1]
      if (now_pos[1] < mini_y) mini_y = now_pos[1]
    })
    return [
      [mini_x, max_x],
      [mini_y, max_y]
    ]
  })

  // function avg_split_color(split_num: number) {
  //   const res = [] as { h: number; s: number; l: number; a: number }[]
  //   const color_s = 100
  //   const color_l = 65
  //   const color_a = 1
  //   const color_h_seg = 360 / split_num
  //   let now_h = 0
  //   for (let i = 0; i < split_num; i += 1) {
  //     res.push({ h: now_h, s: color_s, l: color_l, a: color_a })
  //     now_h += color_h_seg
  //   }
  //   return res
  // }

  // 不同城市 文化圈的颜色
  // 打乱数组
  // function shuffleArray(array: any[]) {
  //   for (let i = array.length - 1; i > 0; i--) {
  //     const j = Math.floor(Math.random() * (i + 1))
  //     ;[array[i], array[j]] = [array[j], array[i]]
  //   }
  //   return array
  // }
  // const cities_colors = computed(() => {
  //   const color_num = cities_names.value.length
  //   const res = avg_split_color(color_num)
  //   return shuffleArray(res)
  // })
  // const culture_groups_colors = computed(() => {
  //   const color_num = culture_groups_names.value.length
  //   const res = avg_split_color(color_num)
  //   return shuffleArray(res)
  // })
  // 所有点的颜色
  const tsne_pts_color = computed(() => {
    const res = [] as { h: number; s: number; l: number; a: number }[]
    if (now_show_status.value == 0) {
      idx2city_idxs.value.forEach((city_idx, data_idx) => {
        if (sel_show_cities.value[city_idx] && sel_show_nodes.value[data_idx]) {
          res.push(cities_colors.value[city_idx])
        } else {
          res.push({ h: 180, s: 100, l: 100, a: 0 })
        }
      })
    } else {
      const other_cul_group_idx = culture_groups_colors.value.length - 1
      idx2culture_group_idxs.value.forEach((culture_group_idx, data_idx) => {
        if (culture_group_idx == -1) culture_group_idx = other_cul_group_idx
        if (sel_show_culture_groups.value[culture_group_idx] && sel_show_nodes.value[data_idx]) {
          res.push(culture_groups_colors.value[culture_group_idx])
        } else {
          res.push({ h: 180, s: 100, l: 100, a: 0 })
        }
      })
    }
    return res
  })

  const std_tsne_pts = computed(() => {
    const nodes = [] as number[][]

    tsne_pos.value.forEach((now_pos, pt_idx) => {
      // 判断是否需要这个点

      let node_x = 0
      if (tsne_range.value[0][0] != tsne_range.value[0][1]) {
        node_x =
          (now_pos[0] - tsne_range.value[0][0]) / (tsne_range.value[0][1] - tsne_range.value[0][0])
      }
      let node_y = 0
      if (tsne_range.value[1][0] != tsne_range.value[1][1]) {
        node_y =
          (now_pos[1] - tsne_range.value[1][0]) / (tsne_range.value[1][1] - tsne_range.value[1][0])
      }
      nodes.push([node_x, node_y])
    })
    return nodes
  })

  // 不同城市的数据
  const std_cities_feats = computed(() => {
    const cities_street_scale = [] as number[][]
    const cities_greenery = [] as number[][]
    cities_names.value.forEach(() => {
      cities_street_scale.push([])
      cities_greenery.push([])
    })

    // street scale数据
    try {
      street_scales.value.forEach((street_scale_val, data_idx) => {
        const city_idx = idx2city_idxs.value[data_idx]
        cities_street_scale[city_idx].push(street_scale_val)
      })

      // greenery数据
      greenery.value.forEach((greenery_val, data_idx) => {
        const city_idx = idx2city_idxs.value[data_idx]
        cities_greenery[city_idx].push(greenery_val)
      })

      return {
        cities_street_scale: cities_street_scale,
        cities_greenery: cities_greenery
      }
    } catch (error) {
      return {
        cities_street_scale: [] as number[][],
        cities_greenery: [] as number[][]
      }
    }
  })

  // 每个文化圈的节点数据
  const cul_group2data_idx = computed(() => {
    const res = [] as number[][]
    culture_groups_names.value.forEach(() => {
      res.push([])
    })
    const other_cul_idx = res.length - 1
    if (res.length == 0) return []
    idx2culture_group_idxs.value.forEach((cul_idx, data_idx) => {
      if (cul_idx == -1) res[other_cul_idx].push(data_idx)
      else res[cul_idx].push(data_idx)
      if (cul_idx == -1) console.log(cities_names.value[idx2city_idxs.value[data_idx]])
    })
    return res
  })

  // 每个城市节点的接近中心性
  const city_closeness_centrality = computed(() => {
    const res = [] as number[]
    const city_num = normalized_cities_conf_matrix.value.length
    for (let i = 0; i < city_num; i += 1) {
      let tmp = 0
      for (let j = 0; j < city_num; j += 1) {
        if (i == j) continue
        tmp += normalized_cities_conf_matrix.value[i][j] + normalized_cities_conf_matrix.value[j][i]
      }
      res.push(tmp / (2 * city_num - 2))
    }
    return res
  })

  // 城市的文化圈
  const cities2cul_group_idx = computed(() => {
    const res = new Array<number>(cities_colors.value.length).fill(-1)
    cities_in_culture_groups.value.forEach((cul_group_cities, cul_group_idx) => {
      cul_group_cities.forEach((city_idx) => {
        res[city_idx] = cul_group_idx
      })
    })
    return res
  })

  return {
    tsne_pos,
    street_scales,
    building_colors,
    facade_material,
    architectural_style,
    greenery,
    urban_sign,
    idx2city_idxs,
    cities_names,
    culture_groups_names,
    cities_in_culture_groups,
    now_show_status,
    sel_show_cities,
    sel_show_culture_groups,
    sel_show_nodes,
    cul_group_status,
    init_all_feats,
    std_tsne_pts,
    cities_colors,
    culture_groups_colors,
    tsne_pts_color,
    std_cities_feats,
    cul_group2data_idx,
    normalized_cities_conf_matrix,
    normalized_cul_groups_conf_matrix,
    cities_pos,
    city_closeness_centrality,
    cities2cul_group_idx,
    cities_tsne_pos
  }
})
