<template>
  <v-chart ref="chartRef" :option="option" autoresize />
</template>

<script setup lang="ts">
import * as echarts from "echarts/core";
import {
  TitleComponent,
  TitleComponentOption,
  DatasetComponent,
  DatasetComponentOption,
  ToolboxComponent,
  ToolboxComponentOption,
  TooltipComponent,
  TooltipComponentOption,
  GridComponent,
  GridComponentOption,
  LegendComponent,
  LegendComponentOption,
} from "echarts/components";
import { LineChart, LineSeriesOption, BarChart, BarSeriesOption } from "echarts/charts";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import type { FeedbackStats } from "@/api/feedback";

echarts.use([
  TitleComponent,
  DatasetComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  BarChart,
  CanvasRenderer,
  UniversalTransition,
]);

type EChartsOption = echarts.ComposeOption<
  | TitleComponentOption
  | DatasetComponentOption
  | ToolboxComponentOption
  | TooltipComponentOption
  | GridComponentOption
  | LegendComponentOption
  | LineSeriesOption
  | BarSeriesOption
>;

const props = defineProps<{ data: FeedbackStats }>();

const chartRef = ref<InstanceType<typeof VChart>>();

const option: EChartsOption = {
  color: ["#f89588", "#7cd6cf", "#9192ab", "#7898e1"],
  title: { text: "聊天反馈统计图" },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "cross",
      crossStyle: { color: "#999" },
    },
  },
  toolbox: {
    feature: {
      dataView: { show: true, readOnly: false },
      magicType: { show: true, type: ["line", "bar"] },
      restore: { show: true },
      saveAsImage: { show: true },
    },
  },
  dataset: {
    dimensions: ["date", "total", "like", "dislike", "comments"],
    source: props.data.by_date,
  },
  legend: {
    data: ["总反馈数", "赞", "踩", "评论"],
  },
  xAxis: [
    {
      type: "category",
      axisPointer: { type: "shadow" },
    },
  ],
  yAxis: [{ type: "value", name: "反馈数", minInterval: 1 }],
  grid: { bottom: 20, left: 60, right: 60 },
  series: [
    { name: "总反馈数", type: "line" },
    { name: "赞", type: "bar" },
    { name: "踩", type: "bar" },
    { name: "评论", type: "bar" },
  ],
};

watch(props, () => {
  (option.dataset as any).source = props.data.by_date;
  chartRef.value?.setOption(option, { notMerge: true });
});
</script>

<style scoped></style>
