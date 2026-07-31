import type { RemainingQuickWinBinding } from './types';

export const remainingQuickWinBindings: readonly RemainingQuickWinBinding[] = [
  {
    "capabilityId": "CAP-6F5DF526EE59",
    "capabilityName": "Admin Only",
    "endpoint": "/api/admin-ui/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-753A055CFA5A",
    "capabilityName": "Ndsp Write Alert State",
    "endpoint": "/api/admin-ui/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-7739F02602D8",
    "capabilityName": "Get User By Id",
    "endpoint": "/api/auth/login/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-784548F2FDAD",
    "capabilityName": "Authorize",
    "endpoint": "/api/admin-actions/users/action/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-790CBD0E1BCE",
    "capabilityName": "Delete User Dependencies",
    "endpoint": "/api/admin/users/action/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-89CA79DDADE2",
    "capabilityName": "Ndsp Read Alert State",
    "endpoint": "/api/admin-ui/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-9866D4AE9D59",
    "capabilityName": "Update User Status",
    "endpoint": "/api/admin-ui/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-A231BBA8D29D",
    "capabilityName": "Auth Required",
    "endpoint": "/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-ACFDAF4DAD5E",
    "capabilityName": "Auth",
    "endpoint": "/api/auth/login/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-DF54F83FC9EB",
    "capabilityName": "Authorize",
    "endpoint": "/api/admin/users/action/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  },
  {
    "capabilityId": "CAP-E22DBA05712A",
    "capabilityName": "Get User By Email",
    "endpoint": "/api/auth/login/health",
    "screen": "TRIAL",
    "component": "RemainingQuickWinPanel",
    "states": [
      "loading",
      "empty",
      "stale",
      "error",
      "ready"
    ]
  }
] as const;
