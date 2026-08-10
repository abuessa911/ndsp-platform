import type { ReactNode } from "react"

import { PublicFooter } from "@/components/ndsp/public-footer"
import { PublicHeader } from "@/components/ndsp/public-header"

type PublicLayoutProps = {
  children: ReactNode
}

export function PublicLayout({ children }: PublicLayoutProps) {
  return (
    <div className="sovereign-app">
      <PublicHeader />
      <main>{children}</main>
      <PublicFooter />
    </div>
  )
}
