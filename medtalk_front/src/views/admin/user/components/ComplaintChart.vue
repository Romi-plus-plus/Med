<template>
  <v-chart ref="chartRef" :option="option" autoresize />
</template>

<script setup lang="ts">
import type { BarSeriesOption } from "echarts/charts";
import { BarChart } from "echarts/charts";
import type {
  TitleComponentOption,
  DatasetComponentOption,
  GridComponentOption,
  LegendComponentOption,
  ToolboxComponentOption,
  TooltipComponentOption,
} from "echarts/components";
import {
  TitleComponent,
  DatasetComponent,
  GridComponent,
  LegendComponent,
  ToolboxComponent,
  TooltipComponent,
} from "echarts/components";
import type { ComposeOption } from "echarts/core";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import type { ComplaintStats } from "@/api/complaint";

use([
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  DatasetComponent,
  LegendComponent,
  GridComponent,
  BarChart,
  CanvasRenderer,
]);

type EChartsOption = ComposeOption<
  | TitleComponentOption
  | TooltipComponentOption
  | ToolboxComponentOption
  | DatasetComponentOption
  | LegendComponentOption
  | GridComponentOption
  | BarSeriesOption
>;

const props = defineProps<{ data: ComplaintStats }>();

const chartRef = ref<InstanceType<typeof VChart>>();

const option: EChartsOption = {
  color: ["#63b2ee", "#76da91"],
  title: { text: "投诉统计图" },
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
      restore: { show: true },
      saveAsImage: { show: true },
    },
  },
  dataset: {
    dimensions: ["date", "creation", "resolution"],
    source: props.data.by_date,
  },
  legend: {
    data: ["创建", "解决"],
  },
  xAxis: [
    {
      type: "category",
      axisPointer: { type: "shadow" },
    },
  ],
  yAxis: [{ type: "value", name: "数量", minInterval: 1 }],
  grid: { bottom: 20, left: 40, right: 40 },
  series: [
    { name: "创建", type: "bar" },
    { name: "解决", type: "bar" },
  ],
};

watch(props, () => {
  (option.dataset as any).source = props.data.by_date;
  chartRef.value?.setOption(option, { notMerge: true });
});
</script>

<style scoped></style>
