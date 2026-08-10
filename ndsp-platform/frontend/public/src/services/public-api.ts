import type { ZodType } from "zod"

import {
  corePublicSchema,
  evidencePayloadSchema,
  marketContextSchema,
  overviewSchema,
  type CorePublic,
  type EvidencePayload,
  type MarketContext,
  type PublicOverview,
} from "@/contracts/public-contracts"

import {
  demoCore,
  demoEvidence,
  demoMarketContext,
  demoOverview,
} from "@/data/public-demo"

const demoMode = import.meta.env.VITE_PUBLIC_DEMO_MODE !== "false"

async function publicRequest<T>(
  path: string,
  schema: ZodType<T>,
  demoValue: T,
): Promise<T> {
  if (demoMode) {
    return schema.parse(demoValue)
  }

  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
    },
  })

  if (!response.ok) {
    throw new Error(`Public API request failed: ${response.status}`)
  }

  return schema.parse(await response.json())
}

export function getPublicOverview(): Promise<PublicOverview> {
  return publicRequest(
    "/api/public/overview",
    overviewSchema,
    demoOverview,
  )
}

export function getPublicCore(): Promise<CorePublic> {
  return publicRequest(
    "/api/public/core",
    corePublicSchema,
    demoCore,
  )
}

export function getMarketContext(): Promise<MarketContext> {
  return publicRequest(
    "/api/public/market-context",
    marketContextSchema,
    demoMarketContext,
  )
}

export function getPublicEvidence(): Promise<EvidencePayload> {
  return publicRequest(
    "/api/public/evidence",
    evidencePayloadSchema,
    demoEvidence,
  )
}
