# Examples

Business case examples illustrating the eCrop standard in use: for each case, a narrative
description of the actors and scope, the specific eCrop operations involved, and example
request/response payloads.

Start a new business case from the [`_template/`](_template/README.md) skeleton — copy it into a
new kebab-case folder here (e.g. `examples/<business-case-slug>/`) and fill it in. Put larger or
reused example payloads in a `payloads/` subfolder next to that case's `README.md`.

| Business case | Actors | Description |
| --- | --- | --- |
| [Supplier inbound delivery registration](supplier-inbound-delivery-registration/README.md) | Supplier employee, supplier delivery system, eCrop server, grower | A supplier's delivery system registers/corrects/cancels inbound deliveries for a grower it's granted access to, keeping the grower's stock on the platform up to date |
| [Farm Management System sync of executed field operations](fms-crop-operations-sync/README.md) | Grower, Farm Management System, eCrop server | A grower's own FMS automatically syncs executed tasks/operations — at both plot and crop level — for plots/crops already registered on the platform, without the grower using it interactively |

See also [`docs/guides/`](../docs/guides/), which currently holds a similar implementation guide
for the Loonwerkportaal use case (`implementatie-instructie-loonwerkportaal.md`) — to be
integrated here later.
