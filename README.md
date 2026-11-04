# Azure Container Apps Album API

This is the companion repository for the [Azure Container Apps code-to-cloud quickstart](https://docs.microsoft.com/en-us/azure/container-apps/quickstart-code-to-cloud?tabs=bash%2Ccsharp&pivots=acr-remote).

This backend Album API sample is available in other languages:

| [C#](https://github.com/azure-samples/containerapps-albumapi-csharp) | [Go](https://github.com/azure-samples/containerapps-albumapi-go) | [JavaScript](https://github.com/azure-samples/containerapps-albumapi-javascript) | [Java](https://github.com/azure-samples/containerapps-albumapi-java) |
| -------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------- |

---

## API Endpoints

The API exposes health and readiness endpoints for monitoring and deployment orchestration.

### `GET /health`

Checks whether the API application is running and responding.

Successful response:

HTTP `200 OK`

```json
{
  "status": "healthy"
}
```

This endpoint does not check database connectivity. It is intended for liveness checks.

### `GET /ready`

Checks whether the API is ready to serve requests by executing a simple database query (`SELECT 1`).

When the database is available:

HTTP `200 OK`

```json
{
  "status": "ready"
}
```

When the database is unavailable:

HTTP `503 Service Unavailable`

```json
{
  "detail": "database unavailable"
}
```

This endpoint is intended for readiness checks. A replica should not receive application traffic when its database dependency is unavailable.

### Why separate health and readiness checks?

An API process can be running while its database connection is unavailable.

Separating these checks allows the platform to distinguish between:

- **Liveness:** Is the application process responding?
- **Readiness:** Can the application currently serve requests?

This is particularly useful when Azure Container Apps starts new replicas, restarts containers, or handles temporary database connectivity issues.
