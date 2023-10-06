<template>
  <v-chart ref="chartRef" :option="option" autoresize />
</template>

<script lang="ts" setup>
import VChart from "vue-echarts";
import * as echarts from "echarts/core";
import { TitleComponent, TitleComponentOption } from "echarts/components";
import { GaugeChart, GaugeSeriesOption } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { FeedbackStats } from "@/api/feedback";

echarts.use([TitleComponent, GaugeChart, CanvasRenderer]);

type EChartsOption = echarts.ComposeOption<TitleComponentOption | GaugeSeriesOption>;

const props = defineProps<{ data: FeedbackStats }>();

const chartRef = ref<InstanceType<typeof VChart>>();

const gaugeData = [
  {
    value: +((props.data.total_like / props.data.total) * 100).toFixed(1),
    name: "👍",
    title: { offsetCenter: ["0%", "-40%"] },
    detail: { valueAnimation: true, offsetCenter: ["0%", "-25%"] },
  },
  {
    value: +((props.data.total_dislike / props.data.total) * 100).toFixed(1),
    name: "👎",
    title: { offsetCenter: ["0%", "-5%"] },
    detail: { valueAnimation: true, offsetCenter: ["0%", "10%"] },
  },
  {
    value: +((props.data.total_comment / props.data.total) * 100).toFixed(1),
    name: "💬",
    title: { offsetCenter: ["0%", "30%"] },
    detail: { valueAnimation: true, offsetCenter: ["0%", "45%"] },
  },
];

const option: EChartsOption = {
  color: ["#efa666", "#63b2ee", "#9987ce"],
  title: { text: "聊天反馈率统计图" },
  series: [
    {
      type: "gauge",
      startAngle: 90,
      endAngle: -270,
      radius: 120,
      pointer: { show: false },
      progress: { show: true, overlap: false, roundCap: true, clip: false },
      axisLine: { lineStyle: { width: 40 } },
      splitLine: { show: false, distance: 0, length: 10 },
      axisTick: { show: false },
      axisLabel: { show: false, distance: 50 },
      data: gaugeData,
      title: { fontSize: 14 },
      detail: {
        width: 40,
        height: 8,
        fontSize: 14,
        color: "inherit",
        borderColor: "inherit",
        borderRadius: 20,
        borderWidth: 1,
        formatter: "{value}%",
      },
    },
  ],
};

watch(props, () => {
  gaugeData[0].value = +((props.data.total_like / props.data.total) * 100).toFixed(1);
  gaugeData[1].value = +((props.data.total_dislike / props.data.total) * 100).toFixed(1);
  gaugeData[2].value = +((props.data.total_comment / props.data.total) * 100).toFixed(1);
  chartRef.value?.setOption({ series: [{ data: gaugeData }] });
});
</script>

<style scoped></style>
