# Issue approval flow

## Trigger

Dataverse: when an Issue row changes to `Submitted`.

## Steps

1. Read Issue, Component and Owner context.
2. Validate mandatory fields: component, description, severity and owner.
3. Confirm required Evidence metadata exists for severities that require evidence.
4. Create an Approval record with `Pending` state.
5. Start an approval assigned to the configured quality approver.
6. On approval:
   - set Issue status to `Approved`;
   - update Approval decision and timestamp;
   - append StatusHistory;
   - notify the issue owner.
7. On rejection:
   - set Issue status to `Rejected`;
   - persist the reviewer comment;
   - append StatusHistory;
   - notify the issue owner.
8. On validation or connector failure:
   - leave the Issue in a recoverable state;
   - write a traceable error note;
   - avoid silently marking the process complete.

## Idempotency

The implementation should use the Issue ID plus current workflow state to prevent duplicate approval creation after retries.
