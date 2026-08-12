import type { PropsWithChildren } from "react";
import { QueryClientProvider } from "@tanstack/react-query";

import "../i18n";
import { queryClient } from "./queryClient";

export function FoundationProviders({
  children
}: PropsWithChildren) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
