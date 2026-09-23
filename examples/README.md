# Examples

Business case examples illustrating the eCrop standard in use: for each case, a narrative
description of the actors and scope, the specific eCrop operations involved, and example
request/response payloads.


| Business case | Actors | Description |
| --- | --- | --- |
| [Supplier inbound delivery registration](supplier-inbound-delivery-registration/README.md) | Supplier employee, supplier delivery system, eCrop server, grower | A supplier's delivery system registers/corrects/cancels inbound deliveries for a grower it's granted access to, keeping the grower's stock on the platform up to date |
| [Farm Management System sync of executed field operations](fms-crop-operations-sync/README.md) | Grower, Farm Management System, eCrop server | A grower's own FMS automatically syncs executed tasks/operations — at both plot and crop level — for plots/crops already registered on the platform, without the grower using it interactively |
| [Contractor planning: retrieving a grower's plots and geometry](contractor-task-planning/README.md) | Contractor employee, Contractor Planning System, eCrop server, grower | A contractor's planning system retrieves a granted grower's plots and their geometry (2 linked calls per plot) to plan field work; registering the performed task is a deferred follow-up phase |

See also [`docs/guides/`](../docs/guides/), which currently holds a similar implementation guide
for the Loonwerkportaal use case (`implementatie-instructie-loonwerkportaal.md`) — to be
integrated here later.
