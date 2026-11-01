# Example domain permission rubric · `guide:permissionrubric:example-domain-rubric`

Everything in this document is fictional. The aliases `sagofink-orchestration` and `mondreiher-analysis`, accounts, roots, and rule identifiers demonstrate format only and identify no live installation.

## Purpose and custody · `sec:permissionrubric:purpose-and-custody`

A domain rubric supplies installation facts the public general rubric cannot know. Only the superloop's orchestrator agent writes it after adjudicating an escalation. The triage hook and classifier model read it but never modify it, and a lane never writes or grants a rule.

Keep the real rubric in the instance repository at `permissions/domain.md`, with its absolute deployed path selected by `PERMISSION_TRIAGE_OWNER_RUBRIC`. Treat it as private policy state. A missing rubric intentionally leaves the general rubric in force, which means installation-specific actions are denied and escalated to the superloop's orchestrator rather than becoming implicitly routine.

## Rule format · `sec:permissionrubric:rule-format`

Write one narrow row per stable operation. Bind every row to an alias or closed alias family, account role, command grammar, allowed root, operand constraints, required whole-command timeout, timing rule, and exclusions. Use a durable rule identifier so journal reviews can name the rule that absorbed an escalation.

|Rule ID|Class|Exact operation boundary|Required guards|Reason|
|-------|-----|------------------------|---------------|------|
|`lane-gate-sagofink`|`routine-superloop`|On `sagofink-orchestration`, change directory to `/srv/loops/orchestration/lanes/checkouts/LANE` and run only the declared linter check or package test.|Bash timeout at most 900 seconds; `BatchMode=yes`; `ConnectTimeout` at most 10 seconds; each build or test begins with `time nice`; `LANE` matches `[a-z0-9-]+`; no `sudo`, redirect, remote change, or extra command.|The alias, account, checkout root, gate family, and evidence shape are registered together.|
|`lane-prepare-sagofink`|`routine-superloop`|On `sagofink-orchestration`, create one named bare lane hub and one checkout below `/srv/loops/orchestration/lanes/`, then set that checkout's origin to the named lane hub.|Bash timeout at most 120 seconds; non-interactive SSH; one `LANE` value matching `[a-z0-9-]+`; source hub fixed at `/srv/git/orchestration.git`; no overwrite, cleanup, privilege, endpoint, or publication.|Disposable lane preparation is repetitive and bounded to one registered root.|
|`registry-notice-read`|`routine-superloop`|On `mondreiher-analysis`, read at most 1,000 bytes from one `.md` file below `/srv/correspondence/inbox/` with `sudo -n head -c`.|Bash timeout at most 30 seconds; non-interactive SSH; basename only; no glob, traversal, `cat`, environment dump, key-like name, or second command.|The owner has designated this bounded notice surface as non-secret operational input.|
|`runtime-registry-sync`|`routine-superloop`|Compare one tracked registry file with one runtime mirror and replace the mirror only when bytes differ.|Local source and destination are exact paths declared on this row in the real rubric; replacement is atomic, mode-preserving, and timed; no instruction, permission, hook, settings, key, or transcript target.|The runtime mirror is derived state with a fixed source and recovery path.|

Never write catch-all rows such as `ssh sagofink-*`, `sudo *`, `rm -rf /srv/*`, “all lane commands,” or “anything the orchestrator requests.” A rule is invalid if a new alias, account, root, verb, privilege, or external destination can match without another adjudication by the superloop's orchestrator.

## Turning journal records into rules · `sec:permissionrubric:journal-to-rules`

The superloop's orchestrator agent runs `permission-triage review` to print unadjudicated escalations oldest first and group repeated normalized shapes. For each group, it decides whether the operation was wrong, is already covered, or is a stable installation routine. It does not copy a credential, endpoint, unique filename, or accidental command batch into the rubric.

For a stable routine, the orchestrator reduces the observed command to its smallest invariant grammar, replaces volatile operands with constrained names, adds the exact alias and root, requires the timeout and timing evidence, lists forbidden expansions, then writes the row manually. It re-runs review against the updated rubric and requires the intended group to become `routine-superloop` while every negative twin remains `suspicious` or `agent-error`.

After writing the rule, the orchestrator records the disposition with `permission-triage review --mark ID adjudicated-rule-added --rule RULE_ID`; the mark names the rule already written. For a rejected escalation it uses `permission-triage review --mark ID adjudicated-rejected --reason TEXT`, and for an `agent-error` that the worker's report proves was repaired and rerun it uses `permission-triage review --mark ID corrected-and-rerun --request-digest DIGEST`. These commands append review evidence only; they never alter the rubric.

## Review checklist · `sec:permissionrubric:review-checklist`

1. The journal outcome is exactly `escalated`, `adjudicated-rule-added`, `adjudicated-rejected`, or `corrected-and-rerun`, and no denied request is treated as having run.
2. The proposed row describes one operation and one failure domain.
3. Alias, account, root, verbs, operands, timeout, timing, privilege, and exclusions are explicit.
4. Secrets, endpoint coordinates, private individual data, and command-specific opaque values are absent.
5. Permission grants, agent-control changes, broad destruction, and authenticated external transactions remain suspicious.
6. A positive fixture matches, and missing-timeout, broader-path, extra-command, wildcard, privilege, and endpoint negative twins do not.
7. Harness deny rules and the general rubric's always-suspicious boundaries still receive independent acceptance probes after the owner rule is present.
