# NDSP Project Structure

Official long-term structure:

- apps/public-site: Astro public website for ndsp.app
- apps/user-portal: Next.js user portal for my.ndsp.app
- apps/admin-console: Next.js admin console for admin.ndsp.app
- backend: FastAPI backend for api.ndsp.app
- packages/ui: shared design tokens
- packages/types: shared TypeScript contracts
- packages/config: shared configuration

Rules:

- Frontend never decides.
- Backend is the source of truth.
- Public website uses Astro.
- User portal uses Next.js.
- Admin console uses Next.js.
- Backend uses FastAPI + PostgreSQL.
- Protected logic never leaves backend.
