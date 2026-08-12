import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom"

import { PublicLayout } from "@/layouts/public-layout"

import { AccountPage } from "@/pages/account-page"
import { CorePage } from "@/pages/core-page"
import { EvidencePage } from "@/pages/evidence-page"
import { HomePage } from "@/pages/home-page"
import { MarketContextPage } from "@/pages/market-context-page"
import { MethodologyPage } from "@/pages/methodology-page"
import { OverviewPage } from "@/pages/overview-page"

export default function App() {
  return (
    <BrowserRouter>
      <PublicLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/overview" element={<OverviewPage />} />
          <Route path="/core" element={<CorePage />} />
          <Route
            path="/market-context"
            element={<MarketContextPage />}
          />
          <Route path="/evidence" element={<EvidencePage />} />
          <Route
            path="/methodology"
            element={<MethodologyPage />}
          />
          <Route path="/account" element={<AccountPage />} />
        </Routes>
      </PublicLayout>
    </BrowserRouter>
  )
}
