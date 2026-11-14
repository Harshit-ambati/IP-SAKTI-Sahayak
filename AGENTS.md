# IP-SAKTI Sahayak agent instructions

Read `docs/work-plan/MASTER_PLAN.md` and the relevant member file under `docs/work-plan/modules/` before changing a phase task. Inspect the live repository and applicable nested instructions. Planning targets and preliminary corpus rows are not evidence that work is complete.

## Mandatory phase gate

The task IDs in each member module (`H-01` through `H-06`, `T-01` through `T-06`, and so on) are sequential phases for that member. Before creating a branch, file, implementation, commit or PR for phase N+1:

1. Verify from GitHub that phase N's PR is **merged into the shared base branch**. Record its PR URL and merge commit in the next phase issue and PR. A draft PR, approval, green check, local commit or closed-unmerged PR does not qualify.
2. If phase N is not merged, proceed only when Harshit has given **explicit written permission before the early start**. The permission must identify the member, next phase/task ID, reason and permitted scope. Link that permission in the issue and next phase PR. For Harshit's own early start, record his decision and obtain Suresh's independent review.
3. If neither condition is verifiable, stop before any next-phase write. Read-only investigation and discussion are allowed. Report the exact blocker. A target week never overrides the gate.

The exception only permits the specified early work. It does not complete the prior phase, waive tests, reviews, citation checks or PR requirements, or authorize merging. The prior phase remains open until its own PR is merged.

## Truth and review

Do not invent official provisions, corpus approval, API contracts, benchmark labels, test results or deployment status. Keep India and international evidence separate; do not serve unreviewed passage summaries as legal-answer evidence. Do not commit secrets, personal formulations or restricted TKDL data. Run available checks and report observed results and failures.

Use a separate branch and draft PR for each completed nonempty phase. Include the phase ID, actual changed files, test commands/results, prior merged PR or exception link, risks and requested reviewers in the PR body. Do not merge a phase without independent review. If no meaningful change is possible, report the blocker; do not claim the phase is complete or create an empty PR.
