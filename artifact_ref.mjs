// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 AlgoVoi (chopmob-cloud). Open A2A primitive, Apache-2.0.
// artifact_ref = "sha256:" + SHA-256(JCS({task_ref, output_hash, artifact_type, produced_at_ms}))
// Recomputes offline with only RFC 8785 (JCS) and SHA-256.
import { createHash } from "node:crypto";
import { canonicalize } from "@algovoi/substrate";

const ARTIFACT_TYPES = new Set(["TEXT", "FILE", "DATA", "ERROR"]);

export function artifactRef(taskRef, outputHash, artifactType, producedAtMs) {
  for (const [name, val] of [["taskRef", taskRef], ["outputHash", outputHash]]) {
    if (typeof val !== "string" || !val.startsWith("sha256:"))
      throw new TypeError(`${name} must be a sha256: string`);
  }
  if (!ARTIFACT_TYPES.has(artifactType))
    throw new TypeError(`artifactType must be one of ${[...ARTIFACT_TYPES].sort().join("|")}`);
  if (!Number.isInteger(producedAtMs) || producedAtMs <= 0)
    throw new TypeError("producedAtMs must be a positive integer");
  const payload = {
    artifact_type: artifactType,
    output_hash: outputHash,
    produced_at_ms: producedAtMs,
    task_ref: taskRef,
  };
  return "sha256:" + createHash("sha256").update(Buffer.from(canonicalize(payload), "utf-8")).digest("hex");
}
