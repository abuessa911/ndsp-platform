import ReactECharts from "echarts-for-react"

type Point = {
  label: string
  value: number
}

type OverviewChartProps = {
  points: Point[]
}

export function OverviewChart({ points }: OverviewChartProps) {
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
      backgroundColor: "#10161b",
      borderColor: "rgba(212,175,55,.35)",
      textStyle: {
        color: "#f5f6f7",
      },
    },
    xAxis: {
      type: "category",
      data: points.map((point) => point.label),
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: "rgba(245,246,247,.12)",
        },
      },
      axisLabel: {
        color: "rgba(245,246,247,.42)",
      },
    },
    yAxis: {
      type: "value",
      splitLine: {
        lineStyle: {
          color: "rgba(245,246,247,.05)",
        },
      },
      axisLabel: {
        color: "rgba(245,246,247,.35)",
      },
    },
    series: [
      {
        type: "line",
        smooth: true,
        data: points.map((point) => point.value),
        symbolSize: 7,
        lineStyle: {
          width: 2,
          color: "#d4af37",
        },
        itemStyle: {
          color: "#29b6f6",
        },
        areaStyle: {
          opacity: 0.1,
          color: "#d4af37",
        },
      },
    ],
  }

  return (
    <ReactECharts
      option={option}
      style={{ height: 350, width: "100%" }}
    />
  )
}
