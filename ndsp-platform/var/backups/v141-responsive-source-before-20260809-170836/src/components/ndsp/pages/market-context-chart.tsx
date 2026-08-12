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
    animationDuration: 900,

    backgroundColor: "transparent",

    grid: {
      top: 25,
      right: 18,
      bottom: 35,
      left: 42,
    },

    tooltip: {
      trigger: "axis",
      backgroundColor: "#070604",
      borderColor: "rgba(120,179,214,.28)",

      textStyle: {
        color: "#f0eeea",
      },
    },

    xAxis: {
      type: "category",

      data: points.map(
        (point) => point.label,
      ),

      axisLine: {
        lineStyle: {
          color: "rgba(240,238,234,.1)",
        },
      },

      axisLabel: {
        color: "rgba(240,238,234,.4)",
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
        color: "rgba(240,238,234,.32)",
      },
    },

    series: [
      {
        type: "bar",

        data: points.map(
          (point) => point.value,
        ),

        barWidth: "36%",

        itemStyle: {
          color: "#78b3d6",
          opacity: 0.56,
        },
      },

      {
        type: "line",

        smooth: true,

        data: points.map(
          (point) => point.value,
        ),

        lineStyle: {
          width: 1.5,
          color: "#c9983f",
        },

        symbolSize: 5,

        itemStyle: {
          color: "#c9983f",
        },
      },
    ],
  }

  return (
    <ReactECharts
      option={option}
      style={{
        height: 390,
        width: "100%",
      }}
    />
  )
}
