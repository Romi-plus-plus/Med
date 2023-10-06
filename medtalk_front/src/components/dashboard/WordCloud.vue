<template>
  <v-chart ref="chartRef" :option="option" autoresize />
</template>

<script setup lang="ts">
import * as echarts from "echarts/core";
import { ToolboxComponent, TooltipComponent, GridComponent } from "echarts/components";
import type { ToolboxComponentOption, TooltipComponentOption, GridComponentOption } from "echarts/components";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import "echarts-wordcloud";

echarts.use([ToolboxComponent, TooltipComponent, GridComponent, CanvasRenderer, UniversalTransition]);

type EChartsOption = echarts.ComposeOption<ToolboxComponentOption | TooltipComponentOption | GridComponentOption>;

const props = defineProps<{ data: { [key: string]: int }; maskImage?: string }>();

const chartRef = ref<InstanceType<typeof VChart>>();

const randomColor = () =>
  "rgb(" +
  [Math.round(Math.random() * 160), Math.round(Math.random() * 160), Math.round(Math.random() * 160)].join(",") +
  ")";

const getHashCode = (str: string) => {
  let hash = 1315423911;
  for (let i = str.length - 1; i >= 0; i--) {
    hash ^= (hash << 5) + str.charCodeAt(i) + (hash >> 2);
  }
  return hash & 0x7fffffff;
};

const hue = (params: any) => (getHashCode(params.name) / 5) % 360;

const maskImage = new Image();
if (props.maskImage) maskImage.src = props.maskImage;

const option: EChartsOption = {
  tooltip: {},
  toolbox: {
    feature: {
      dataView: { show: true, readOnly: false },
      saveAsImage: { show: true },
    },
  },
  series: [
    {
      type: "wordCloud",

      // The shape of the "cloud" to draw. Can be any polar equation represented as a
      // callback function, or a keyword present. Available presents are circle (default),
      // cardioid (apple or heart shape curve, the most known polar equation), diamond (
      // alias of square), triangle-forward, triangle, (alias of triangle-upright, pentagon, and star.

      shape: "circle",

      // Keep aspect ratio of maskImage or 1:1 for shapes
      // This option is supported from echarts-wordcloud@2.1.0
      keepAspect: false,

      // A silhouette image which the white area will be excluded from drawing texts.
      // The shape option will continue to apply as the shape of the cloud to grow.

      maskImage: props.maskImage ? maskImage : undefined,

      // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
      // Default to be put in the center and has 75% x 80% size.

      left: "center",
      top: "center",
      width: "90%",
      height: "90%",
      right: null,
      bottom: null,

      // Text size range which the value in data will be mapped to.
      // Default to have minimum 12px and maximum 60px size.

      sizeRange: [12, 60],

      // Text rotation range and step in degree. Text will be rotated randomly in range [-90, 90] by rotationStep 45

      rotationRange: [0, 0],
      rotationStep: 0,

      // size of the grid in pixels for marking the availability of the canvas
      // the larger the grid size, the bigger the gap between words.

      gridSize: 8,

      // set to true to allow word being draw partly outside of the canvas.
      // Allow word bigger than the size of the canvas to be drawn
      drawOutOfBound: false,

      // if the font size is too large for the text to be displayed,
      // whether to shrink the text. If it is set to false, the text will
      // not be rendered. If it is set to true, the text will be shrinked.
      shrinkToFit: true,

      // If perform layout animation.
      // NOTE disable it will lead to UI blocking when there is lots of words.
      layoutAnimation: true,

      // Global text style
      textStyle: {
        fontFamily: "sans-serif",
        fontWeight: "bold",
        // Color can be a callback function or a color string
        color: (params: any) => `hsl(${hue(params)}, 50%, 50%)`,
      },
      emphasis: {
        // focus: "self",

        textStyle: {
          color: "#528",
          textShadowBlur: 4,
          textShadowColor: "#777",
        },
      },

      // Data is an array. Each array item must have name and value property.
      data: [],
    },
  ],
};

watch(props, () => {
  const data = Object.entries(props.data).map((t) => ({ name: t[0], value: t[1] }));
  chartRef.value?.setOption({ series: [{ data }] });
});
</script>

<style scoped></style>
