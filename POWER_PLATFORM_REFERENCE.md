# Quality Issue & Inspection Management App — Power Platform Reference

A public-safe **design/reference implementation** for an industrial quality workflow using Power Apps/Dataverse/Power Automate/SharePoint concepts.

## Architecture

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

## Inspectable evidence

- [Dataverse table model](schema/dataverse_tables.yaml)
- [Power Fx issue-form patterns](powerfx/issue_form.md)
- [Approval-flow design](flows/issue_approval_flow.md)
- [Governance, ALM and security](governance/ALM_AND_SECURITY.md)
- [Architecture notes](docs/architecture.md)
- [Conceptual UI wireframe](docs/ui_mockup.svg)
- [Synthetic sample records](samples/issues.csv)
- [Validation script](scripts/validate_docs.py)
- [Limitations](LIMITATIONS.md)

## Verification

The repository's **Power Platform portfolio validation** GitHub Actions workflow validates the root reference implementation. Latest verified run observed during the application-system audit: **36719615141 — success**.

## Evidence boundary

This is portfolio/design evidence, not a tenant export and not a claim of professional Power Apps/Dataverse delivery. A real app screenshot, Dataverse environment, connection references and deployable solution package should only be added after the app is instantiated in a user-controlled personal/developer tenant.
