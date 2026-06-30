# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 AlgoVoi (chopmob-cloud). Open A2A primitive, Apache-2.0.
"""artifact_ref: a deterministic, content addressed reference to an A2A Task output.

artifact_ref = "sha256:" + SHA-256(JCS({task_ref, output_hash, artifact_type, produced_at_ms}))

Recomputes offline with only RFC 8785 (JCS) and SHA-256.

Fields
------
task_ref         sha256: reference to the task that produced this artifact (task_ref_v1)
output_hash      sha256: SHA-256 of the raw artifact content bytes
artifact_type    one of: TEXT | FILE | DATA | ERROR
produced_at_ms   integer milliseconds since Unix epoch (must be > 0)
"""
import hashlib
from algovoi_substrate import canonicalize

ARTIFACT_REF_VERSION = "artifact_ref_v1"
ARTIFACT_TYPES = {"TEXT", "FILE", "DATA", "ERROR"}


def artifact_ref(task_ref: str, output_hash: str, artifact_type: str, produced_at_ms: int) -> str:
    for name, val in (("task_ref", task_ref), ("output_hash", output_hash)):
        if not isinstance(val, str) or not val.startswith("sha256:"):
            raise ValueError(f"{name} must be a sha256: string")
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError(f"artifact_type must be one of {sorted(ARTIFACT_TYPES)}")
    if not isinstance(produced_at_ms, int) or produced_at_ms <= 0:
        raise ValueError("produced_at_ms must be a positive integer")
    payload = {
        "artifact_type": artifact_type,
        "output_hash": output_hash,
        "produced_at_ms": produced_at_ms,
        "task_ref": task_ref,
    }
    return "sha256:" + hashlib.sha256(canonicalize(payload).encode("utf-8")).hexdigest()
