# SSADM Notes

## Data Flow

System metrics and access events move from operational services into the FastAPI bridge, then into PostgreSQL. Agents query this structured memory to detect incidents and produce recommendations.

## Logical Data Model

- `user_profiles`: role-aware users for future RBAC.
- `access_logs`: security and activity evidence.
- `system_metrics`: performance and availability measurements.
- `incidents`: detected events and remediation evidence.

## Security Considerations

- No secrets are committed to GitHub.
- Database credentials are supplied through environment variables.
- Destructive database actions are not exposed through the API.
- Agent tools must use validated, read-focused database access.

