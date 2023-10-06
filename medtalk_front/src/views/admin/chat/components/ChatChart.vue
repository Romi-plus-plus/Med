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
import type { ChatStats } from "@/api/chat";

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

const props = defineProps<{ data: ChatStats }>();

const chartRef = ref<InstanceType<typeof VChart>>();

const option: EChartsOption = {
  color: ["#0082fc", "#fdd845", "#22ed7c", "#09b0d3", "#1d27c9"],
  title: { text: "聊天会话消息统计图" },
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
    dimensions: ["date", "total_chats", "total_messages", "questions", "answers", "notes"],
    source: props.data.by_date,
  },
  legend: {
    data: ["总会话数", "总消息数", "提问", "回答", "笔记"],
  },
  xAxis: [
    {
      type: "category",
      axisPointer: { type: "shadow" },
    },
  ],
  yAxis: [{ type: "value", name: "数量", minInterval: 1 }],
  grid: { bottom: 20, left: 60, right: 60 },
  series: [
    { name: "总会话数", type: "line" },
    { name: "总消息数", type: "line" },
    { name: "提问", type: "bar" },
    { name: "回答", type: "bar" },
    { name: "笔记", type: "bar" },
  ],
};

watch(props, () => {
  (option.dataset as any).source = props.data.by_date;
  chartRef.value?.setOption(option, { notMerge: true });
});
</script>

<style scoped></style>
