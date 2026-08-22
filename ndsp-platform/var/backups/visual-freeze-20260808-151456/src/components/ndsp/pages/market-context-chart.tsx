import ReactECharts from "echarts-for-react"

type Point = {
  label: string
  value: number
}

type MarketContextChartProps = {
  points: Point[]
}

export function MarketContextChart({
  points,
}: MarketContextChartProps) {
  const option = {
    backgroundColor: "transparent",
    animationDuration: 1000,
    grid: {
      top: 25,
      right: 18,
      bottom: 35,
      left: 42,
    },
    tooltip: {
      trigger: "axis",
      backgroundColor: "#10161b",
      borderColor: "rgba(41,182,246,.25)",
      textStyle: {
        color: "#f5f6f7",
      },
    },
    xAxis: {
      type: "category",
      data: points.map((item) => item.label),
      axisLine: {
        lineStyle: {
          color: "rgba(245,246,247,.1)",
        },
      },
      axisLabel: {
        color: "rgba(245,246,247,.4)",
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
        color: "rgba(245,246,247,.32)",
      },
    },
    series: [
      {
        type: "bar",
        data: points.map((item) => item.value),
        barWidth: "38%",
        itemStyle: {
          color: "#327d9f",
          borderRadius: [4, 4, 0, 0],
        },
      },
      {
        type: "line",
        smooth: true,
        data: points.map((item) => item.value),
        lineStyle: {
          width: 2,
          color: "#d4af37",
        },
        symbolSize: 6,
        itemStyle: {
          color: "#e6c66f",
        },
      },
    ],
  }

  return (
    <ReactECharts
      option={option}
      style={{ height: 390, width: "100%" }}
    />
  )
}
