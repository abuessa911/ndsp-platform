import { useMemo } from "react"

import {
  AllCommunityModule,
  ModuleRegistry,
  themeQuartz,
  type ColDef,
} from "ag-grid-community"

import { AgGridReact } from "ag-grid-react"

import type {
  EvidenceRow,
} from "@/contracts/public-contracts"

ModuleRegistry.registerModules([
  AllCommunityModule,
])

const sovereignGridTheme =
  themeQuartz.withParams({
    backgroundColor: "#070604",
    foregroundColor: "#f0eeea",

    headerBackgroundColor: "#0c0b08",
    headerTextColor: "#c9983f",

    borderColor:
      "rgba(201,152,63,.18)",

    rowHoverColor:
      "rgba(120,179,214,.045)",

    fontFamily:
      "IBM Plex Sans, Noto Sans Arabic, Segoe UI, Arial, sans-serif",
  })

type EvidenceGridProps = {
  rows: EvidenceRow[]
}

export function EvidenceGrid({
  rows,
}: EvidenceGridProps) {
  const columnDefs =
    useMemo<ColDef<EvidenceRow>[]>(
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

          valueFormatter: ({
            value,
          }) =>
            value
              ? new Intl.DateTimeFormat(
                  "ar-SA",
                  {
                    dateStyle: "medium",
                    timeStyle: "short",
                  },
                ).format(
                  new Date(value),
                )
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
