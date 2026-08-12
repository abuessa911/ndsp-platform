import ReactECharts from "echarts-for-react"

type Point = {
  label: string
  value: number
}

type OverviewChartProps = {
  points: Point[]
}

export function OverviewChart({
  points,
}: OverviewChartProps) {
  const option = {
    animationDuration: 900,

    backgroundColor: "transparent",

    grid: {
      top: 24,
      right: 15,
      bottom: 34,
      left: 40,
    },

    tooltip: {
      trigger: "axis",
      backgroundColor: "#070604",
      borderColor: "rgba(201,152,63,.35)",
      textStyle: {
        color: "#f0eeea",
      },
    },

    xAxis: {
      type: "category",
      data: points.map((point) => point.label),
      boundaryGap: false,

      axisLine: {
        lineStyle: {
          color: "rgba(240,238,234,.12)",
        },
      },

      axisLabel: {
        color: "rgba(240,238,234,.42)",
      },
    },

    yAxis: {
      type: "value",

      splitLine: {
        lineStyle: {
          color: "rgba(240,238,234,.05)",
        },
      },

      axisLabel: {
        color: "rgba(240,238,234,.34)",
      },
    },

    series: [
      {
        type: "line",
        smooth: true,

        data: points.map(
          (point) => point.value,
        ),

        symbolSize: 6,

        lineStyle: {
          width: 1.5,
          color: "#c9983f",
        },

        itemStyle: {
          color: "#78b3d6",
        },

        areaStyle: {
          opacity: 0.06,
          color: "#c9983f",
        },
      },
    ],
  }

  return (
    <ReactECharts
      option={option}
      style={{
        height: 350,
        width: "100%",
      }}
    />
  )
}
