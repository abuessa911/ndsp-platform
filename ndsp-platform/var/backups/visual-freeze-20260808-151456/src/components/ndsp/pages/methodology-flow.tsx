import {
  Background,
  Controls,
  MarkerType,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react"

import "@xyflow/react/dist/style.css"

const nodes: Node[] = [
  {
    id: "institutional",
    position: { x: 0, y: 0 },
    data: { label: "بيانات مؤسسية" },
  },
  {
    id: "analysis",
    position: { x: 0, y: 90 },
    data: { label: "تقارير وتحليلات" },
  },
  {
    id: "operations",
    position: { x: 0, y: 180 },
    data: { label: "سياق تشغيلي" },
  },
  {
    id: "external",
    position: { x: 0, y: 270 },
    data: { label: "معلومات خارجية" },
  },
  {
    id: "policy",
    position: { x: 0, y: 360 },
    data: { label: "معايير وسياسات" },
  },
  {
    id: "core",
    position: { x: 340, y: 180 },
    data: { label: "CORE" },
    className: "sovereign-flow-core",
  },
  {
    id: "direction",
    position: { x: 640, y: 180 },
    data: { label: "الاتجاه الرسمي" },
    className: "sovereign-flow-direction",
  },
]

const sourceIds = [
  "institutional",
  "analysis",
  "operations",
  "external",
  "policy",
]

const edges: Edge[] = [
  ...sourceIds.map((source) => ({
    id: `${source}-core`,
    source,
    target: "core",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
    style: {
      stroke: "#327d9f",
    },
  })),
  {
    id: "core-direction",
    source: "core",
    target: "direction",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
    style: {
      stroke: "#d4af37",
      strokeWidth: 2,
    },
  },
]

export function MethodologyFlow() {
  return (
    <div className="sovereign-flow">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        minZoom={0.5}
        maxZoom={1.4}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        proOptions={{
          hideAttribution: true,
        }}
      >
        <Background
          gap={28}
          size={1}
          color="rgba(245,246,247,.05)"
        />

        <Controls
          showInteractive={false}
          position="bottom-left"
        />
      </ReactFlow>
    </div>
  )
}
