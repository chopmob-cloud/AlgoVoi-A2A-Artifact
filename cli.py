# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 AlgoVoi (chopmob-cloud). Apache-2.0.
"""Compute artifact_ref from task_ref, output_hash, artifact_type and produced_at_ms.

Usage:
  python cli.py <task_ref> <output_hash> <artifact_type> <produced_at_ms>
"""
import sys
from artifact_ref import artifact_ref

def main():
    if len(sys.argv) != 5:
        print("usage: python cli.py <task_ref> <output_hash> <artifact_type> <produced_at_ms>", file=sys.stderr)
        sys.exit(1)
    print(artifact_ref(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])))

if __name__ == "__main__":
    main()
