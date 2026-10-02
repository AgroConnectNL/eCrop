# Use cases

Business cases illustrating the eCrop standard in use. Each case has its own folder with:

- `README.md` — a narrative description of the actors and scope, the specific eCrop operations
  involved, and example request/response payloads (see [`_template`](_template/README.md));
- `examples.yaml` — the example overrides (e.g. identifier schemes) for this case's distribution of
  the OpenAPI specification, see [`openapi/README.md`](../openapi/README.md);
- optionally an implementation guide.


| Business case | Actors | Description |
| --- | --- | --- |
| [Supplier inbound delivery registration](supplier-inbound-delivery-registration/README.md) | Supplier employee, supplier delivery system, eCrop server, grower | A supplier's delivery system registers/corrects/cancels inbound deliveries for a grower it's granted access to, keeping the grower's stock on the platform up to date |
| [Farm Management System sync of executed field operations](fms-crop-operations-sync/README.md) | Grower, Farm Management System, eCrop server | A grower's own FMS automatically syncs executed tasks/operations — at both plot and crop level — for plots/crops already registered on the platform, without the grower using it interactively |
| [Contractor planning: retrieving a grower's plots and geometry](contractor-task-planning/README.md) | Contractor employee, Contractor Planning System, eCrop server, grower | A contractor's planning system retrieves a granted grower's plots and their geometry (2 linked calls per plot) to plan field work, and afterwards registers (POST), updates (PUT, optionally PATCH) or deletes the tasks performed on those plots |

The Loonwerkportaal implementation guide for the contractor case (in Dutch) is
[`contractor-task-planning/implementatie-instructie.nl.md`](contractor-task-planning/implementatie-instructie.nl.md).
