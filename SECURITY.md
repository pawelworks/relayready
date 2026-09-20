# Security policy

## Supported versions

RelayReady is pre-release software. Security fixes will be applied to the latest development version.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Email
[lucian.pavel@pawelworks.com](mailto:lucian.pavel@pawelworks.com), addressed to
**Pavel Mihai Lucian**, with the subject `RelayReady security report`. Include
the affected version, a description, reproduction steps, impact, and any
suggested mitigation. Do not send passwords, access tokens or private user data.

This is the owner's approved private reporting route. Delivery and response
times have not been tested; no response-time guarantee is made. The project has
one security contact and no independently staffed security team.

The maintainer will assess reports, coordinate fixes and disclosure with the
reporter, and publish an advisory when appropriate. Please avoid public details
until disclosure is coordinated. GitHub private vulnerability reporting is enabled
and was verified for `pawelworks/relayready`. The repository is still awaiting its
initial source push; email remains an available private reporting route.

## Scope and limitations

The validator checks supplied artifacts; it does not authenticate senders,
authorize execution, enforce policy on external systems, or prove observations
are true. Browser results and mock benchmarks are explicitly demonstrations.
No independent security audit or OpenSSF badge is claimed. See
[the release checklist](docs/RELEASE_CHECKLIST.md) for outstanding assurance work.
