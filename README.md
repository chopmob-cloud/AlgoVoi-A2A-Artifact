# artifact_ref

A deterministic, content addressed reference to an A2A Task output.

    artifact_ref = "sha256:" + SHA-256(JCS({task_ref, output_hash, artifact_type, produced_at_ms}))

Recomputes offline with only RFC 8785 (JCS) and SHA-256. No JWS, no JWKS, no key infrastructure.

## Why

A2A produces Artifacts as task outputs, but nothing makes the output tamper-evident or binds it
to the task that produced it. artifact_ref closes that gap: it is the content address of exactly
which task ran and what it produced.

Composing onto task_ref (AlgoVoi-A2A-Task): the task_ref field pins the exact task delegation
bytes, so an artifact_ref transitively binds agent identity, task instruction, and output.

## Fields

| Field | Type | Description |
|---|---|---|
| `task_ref` | sha256: string | task_ref of the task that produced this artifact (task_ref_v1) |
| `output_hash` | sha256: string | SHA-256 of the raw artifact content bytes |
| `artifact_type` | string | one of: `TEXT` \| `FILE` \| `DATA` \| `ERROR` |
| `produced_at_ms` | integer | milliseconds since Unix epoch, must be > 0 |

## Construction

JCS (RFC 8785) sorts keys lexicographically before hashing, so the field order in the preimage
is always: `artifact_type`, `output_hash`, `produced_at_ms`, `task_ref`.

## Use

Python:

    from artifact_ref import artifact_ref
    ref = artifact_ref(task_ref, output_hash, artifact_type, produced_at_ms)

Node:

    import { artifactRef } from "./artifact_ref.mjs";
    const ref = artifactRef(taskRef, outputHash, artifactType, producedAtMs);

CLI:

    python cli.py <task_ref> <output_hash> <artifact_type> <produced_at_ms>

## Conformance

Vectors live in the algovoi-jcs-conformance-vectors corpus, set artifact_ref_v1: positives,
invariants (field reorder does not change output), and negatives (invalid artifact_type, changed
task_ref, changed output_hash, zero timestamp), verified byte for byte across independent Python
and Node runners.

## Composition

    card_ref  →  task_ref  →  artifact_ref

card_ref (AlgoVoi-A2A-Card) pins who the agent is. task_ref (AlgoVoi-A2A-Task) pins what they
were asked to do. artifact_ref pins what they produced. All three recompute offline from retained bytes.

## License

Apache 2.0. Copyright (c) 2026 AlgoVoi (chopmob-cloud).

artifact_ref is published as a standalone open primitive. This repository provides the reference and its conformance only.
