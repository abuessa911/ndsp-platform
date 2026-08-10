import "@xyflow/react/dist/style.css"

import {
  Background,
  Controls,
  MarkerType,
  Position,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react"

const desktopNodes: Node[] = [
  {
    id: "context",
    position: { x: 20, y: 100 },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    className: "sovereign-flow-node",
    data: {
      label: "السياق",
    },
  },
  {
    id: "evidence",
    position: { x: 310, y: 100 },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    className: "sovereign-flow-node",
    data: {
      label: "الأدلة المصرح بها",
    },
  },
  {
    id: "projection",
    position: { x: 600, y: 100 },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    className: "sovereign-flow-node",
    data: {
      label: "Public Projection",
    },
  },
  {
    id: "core",
    position: { x: 890, y: 100 },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    className:
      "sovereign-flow-node sovereign-flow-node--core",
    data: {
      label: "CORE",
    },
  },
]

const desktopEdges: Edge[] = [
  {
    id: "context-evidence",
    source: "context",
    target: "evidence",
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "evidence-projection",
    source: "evidence",
    target: "projection",
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "projection-core",
    source: "projection",
    target: "core",
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
]

const mobileSteps = [
  {
    id: "01",
    title: "السياق",
    description: "تحديد السياق العام المصرح به.",
  },
  {
    id: "02",
    title: "الأدلة",
    description: "تجميع الأدلة العامة القابلة للتحقق.",
  },
  {
    id: "03",
    title: "Public Projection",
    description: "إسقاط عام محكوم دون كشف المنطق الداخلي.",
  },
  {
    id: "04",
    title: "CORE",
    description: "إصدار الاتجاه الرسمي المصرح به.",
  },
]

export function MethodologyFlow() {
  return (
    <div className="sovereign-flow">
      <div
        className="sovereign-flow__desktop"
        aria-label="المسار المفاهيمي العام"
      >
        <ReactFlow
          nodes={desktopNodes}
          edges={desktopEdges}
          fitView
          fitViewOptions={{
            padding: 0.16,
            minZoom: 0.65,
            maxZoom: 1.1,
          }}
          minZoom={0.55}
          maxZoom={1.25}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
          panOnDrag
          zoomOnScroll={false}
          zoomOnPinch
          preventScrolling={false}
          proOptions={{
            hideAttribution: true,
          }}
        >
          <Background gap={24} size={1} />
          <Controls
            position="bottom-left"
            showInteractive={false}
          />
        </ReactFlow>
      </div>

      <ol className="sovereign-flow__mobile">
        {mobileSteps.map((step, index) => (
          <li
            className={
              index === mobileSteps.length - 1
                ? "sovereign-flow-step sovereign-flow-step--core"
                : "sovereign-flow-step"
            }
            key={step.id}
          >
            <span className="sovereign-flow-step__number">
              {step.id}
            </span>

            <div>
              <strong dir={step.title === "CORE" ? "ltr" : undefined}>
                {step.title}
              </strong>
              <p>{step.description}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}
