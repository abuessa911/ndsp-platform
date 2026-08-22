import { z } from "zod"

export const publicModeSchema = z.enum(["demo", "live"])

export const kpiSchema = z.object({
  id: z.string(),
  label: z.string(),
  value: z.string(),
  detail: z.string(),
  status: z.enum(["neutral", "positive", "warning"]),
})

export const trendPointSchema = z.object({
  label: z.string(),
  value: z.number(),
})

export const overviewSchema = z.object({
  mode: publicModeSchema,
  updatedAt: z.string(),
  kpis: z.array(kpiSchema),
  trend: z.array(trendPointSchema),
})

export const corePublicSchema = z.object({
  mode: publicModeSchema,
  updatedAt: z.string(),
  direction: z.string(),
  summary: z.string(),
  governanceStatus: z.string(),
  evidenceStatus: z.string(),
  freshnessStatus: z.string(),
})

export const marketContextSchema = z.object({
  mode: publicModeSchema,
  updatedAt: z.string(),
  title: z.string(),
  summary: z.string(),
  contextSeries: z.array(trendPointSchema),
})

export const evidenceRowSchema = z.object({
  id: z.string(),
  source: z.string(),
  category: z.string(),
  status: z.string(),
  freshness: z.string(),
  updatedAt: z.string(),
})

export const evidencePayloadSchema = z.object({
  mode: publicModeSchema,
  updatedAt: z.string(),
  rows: z.array(evidenceRowSchema),
})

export type PublicOverview = z.infer<typeof overviewSchema>
export type CorePublic = z.infer<typeof corePublicSchema>
export type MarketContext = z.infer<typeof marketContextSchema>
export type EvidenceRow = z.infer<typeof evidenceRowSchema>
export type EvidencePayload = z.infer<typeof evidencePayloadSchema>
