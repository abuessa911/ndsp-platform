import {
  lazy,
  Suspense,
} from "react"

import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom"

import {
  PublicLayout,
} from "@/layouts/public-layout"

const HomePage = lazy(() =>
  import("@/pages/home-page").then(
    (module) => ({
      default: module.HomePage,
    }),
  ),
)

const OverviewPage = lazy(() =>
  import("@/pages/overview-page").then(
    (module) => ({
      default: module.OverviewPage,
    }),
  ),
)

const CorePage = lazy(() =>
  import("@/pages/core-page").then(
    (module) => ({
      default: module.CorePage,
    }),
  ),
)

const MarketContextPage = lazy(() =>
  import(
    "@/pages/market-context-page"
  ).then((module) => ({
    default:
      module.MarketContextPage,
  })),
)

const EvidencePage = lazy(() =>
  import("@/pages/evidence-page").then(
    (module) => ({
      default: module.EvidencePage,
    }),
  ),
)

const MethodologyPage = lazy(() =>
  import(
    "@/pages/methodology-page"
  ).then((module) => ({
    default:
      module.MethodologyPage,
  })),
)

const AccountPage = lazy(() =>
  import("@/pages/account-page").then(
    (module) => ({
      default: module.AccountPage,
    }),
  ),
)

function RouteLoadingFallback() {
  return (
    <div
      className="sovereign-page-loading"
      role="status"
      aria-live="polite"
    >
      جارٍ تحميل واجهة NDSP…
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <PublicLayout>
        <Suspense
          fallback={
            <RouteLoadingFallback />
          }
        >
          <Routes>
            <Route
              path="/"
              element={<HomePage />}
            />

            <Route
              path="/overview"
              element={<OverviewPage />}
            />

            <Route
              path="/core"
              element={<CorePage />}
            />

            <Route
              path="/market-context"
              element={
                <MarketContextPage />
              }
            />

            <Route
              path="/evidence"
              element={<EvidencePage />}
            />

            <Route
              path="/methodology"
              element={
                <MethodologyPage />
              }
            />

            <Route
              path="/account"
              element={<AccountPage />}
            />
          </Routes>
        </Suspense>
      </PublicLayout>
    </BrowserRouter>
  )
}
