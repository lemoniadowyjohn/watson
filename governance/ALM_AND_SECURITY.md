# ALM and security design

## Environments

Use separate Development, Test and Production environments. Build unmanaged solutions in Development and promote managed solutions through Test before Production.

## Solution contents

- canvas app;
- Dataverse tables, columns and relationships;
- cloud flow;
- connection references;
- environment variables;
- security roles.

## Security roles

- **Reporter** — create/read own issues and upload evidence;
- **Inspector** — create inspections and update assigned issues;
- **Approver** — read relevant issues and create approval decisions;
- **Quality Admin** — administer configuration and reference data.

## Governance rules

- avoid hard-coded environment identifiers;
- use environment variables and connection references;
- apply least privilege;
- validate flow ownership after import;
- retain auditable status and approval history;
- keep corporate exports and tenant-specific configuration out of the public repository.
