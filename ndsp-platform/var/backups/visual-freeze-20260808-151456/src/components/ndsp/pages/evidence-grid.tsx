import { useMemo } from "react"

import {
  AllCommunityModule,
  ModuleRegistry,
  themeQuartz,
  type ColDef,
} from "ag-grid-community"

import { AgGridReact } from "ag-grid-react"

import type { EvidenceRow } from "@/contracts/public-contracts"

ModuleRegistry.registerModules([AllCommunityModule])

const sovereignGridTheme = themeQuartz.withParams({
  backgroundColor: "#0d1318",
  foregroundColor: "#dfe2e4",
  headerBackgroundColor: "#10161b",
  headerTextColor: "#d4af37",
  borderColor: "rgba(245,246,247,.1)",
  rowHoverColor: "rgba(41,182,246,.06)",
  fontFamily: "IBM Plex Sans Arabic, Segoe UI, Arial, sans-serif",
})

type EvidenceGridProps = {
  rows: EvidenceRow[]
}

export function EvidenceGrid({ rows }: EvidenceGridProps) {
  const columnDefs = useMemo<ColDef<EvidenceRow>[]>(
    () => [
      {
        field: "id",
        headerName: "المرجع",
        maxWidth: 130,
      },
      {
        field: "category",
        headerName: "الفئة",
        minWidth: 180,
      },
      {
        field: "source",
        headerName: "المصدر",
        minWidth: 180,
      },
      {
        field: "status",
        headerName: "الحالة",
        minWidth: 130,
      },
      {
        field: "freshness",
        headerName: "الحداثة",
        minWidth: 130,
      },
      {
        field: "updatedAt",
        headerName: "آخر تحديث",
        minWidth: 190,
        valueFormatter: ({ value }) =>
          value
            ? new Intl.DateTimeFormat("ar-SA", {
                dateStyle: "medium",
                timeStyle: "short",
              }).format(new Date(value))
            : "—",
      },
    ],
    [],
  )

  return (
    <div className="sovereign-grid-wrap">
      <AgGridReact<EvidenceRow>
        theme={sovereignGridTheme}
        rowData={rows}
        columnDefs={columnDefs}
        defaultColDef={{
          flex: 1,
          sortable: true,
          filter: true,
          resizable: true,
        }}
        domLayout="autoHeight"
        rowHeight={58}
        headerHeight={52}
      />
    </div>
  )
}
