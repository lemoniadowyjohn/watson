# Quality Issue & Inspection Management App

A public-safe Power Platform portfolio reference implementation for an industrial quality workflow.

## Use case

```text
Power Apps issue form
        |
Dataverse Issue record
        |
validation + ownership
        |
Power Automate approval
        |
SharePoint evidence storage
        |
status + audit history
        |
notification
```

## Scope

The design covers Component, Inspection, Issue, Evidence, Approval and Status History records; Power Apps validation/search patterns; an approval flow; SharePoint evidence separation; role concepts; and ALM/governance considerations.

## Important evidence boundary

This repository is **portfolio/project evidence**. It does not claim that Power Apps or Dataverse were previously delivered in the user's employer environment. No corporate tenant export, proprietary flow package, customer data, credentials, environment IDs or internal URLs are included.

A real app screenshot is intentionally not fabricated. Screenshots should only be added after the app is instantiated in a personal/developer environment.

## Repository map

- `schema/dataverse_tables.yaml` — normalized entity model;
- `powerfx/issue_form.md` — representative Power Fx validation/submission patterns;
- `flows/issue_approval_flow.md` — flow design and failure handling;
- `governance/ALM_AND_SECURITY.md` — environments, roles, DLP and deployment controls;
- `samples/issues.csv` — synthetic sample records;
- `scripts/validate_docs.py` — repository quality/safety validation.

## Target roles

Process Automation · Power Platform · Industrial Digitalisation · Technical Project Engineering
