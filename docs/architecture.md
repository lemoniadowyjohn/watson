# Architecture

```mermaid
flowchart LR
  A[Power Apps] --> B[Dataverse: Issue]
  B --> C[Power Automate validation]
  C --> D[Approval]
  D -->|approved| E[Status update]
  D -->|rejected| F[Rework state]
  A --> G[SharePoint evidence library]
  E --> H[Status History]
  F --> H
  E --> I[Teams / email notification]
  F --> I
```

## Design principles

- Dataverse owns structured transactional state.
- SharePoint stores larger evidence files rather than embedding them in the main Issue table.
- Approval decisions are written back as separate auditable records.
- Status transitions append a StatusHistory record.
- The app design separates maker convenience from governance requirements.
