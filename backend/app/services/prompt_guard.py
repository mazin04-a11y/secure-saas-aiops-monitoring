from dataclasses import dataclass


BLOCKED_TERMS = {
    "drop table",
    "delete from",
    "truncate",
    "alter table",
    "update users",
    "export secrets",
    "show api key",
    "ignore safeguards",
    "bypass",
    "disable guardrails",
}


@dataclass(frozen=True)
class GuardedPrompt:
    original: str
    normalized: str
    accepted: bool
    reason: str


def guard_prompt(prompt: str | None) -> GuardedPrompt:
    original = (prompt or "").strip()
    normalized = " ".join(original.lower().split())

    if not original:
        return GuardedPrompt(
            original="",
            normalized="",
            accepted=True,
            reason="No mission prompt supplied. Default AIOps assessment used.",
        )

    if len(original) > 500:
        return GuardedPrompt(
            original=original[:500],
            normalized=normalized[:500],
            accepted=False,
            reason="Mission prompt rejected because it is longer than the 500 character safety limit.",
        )

    blocked = next((term for term in BLOCKED_TERMS if term in normalized), None)
    if blocked:
        return GuardedPrompt(
            original=original,
            normalized=normalized,
            accepted=False,
            reason=f"Mission prompt rejected because it requested a blocked operation: {blocked}.",
        )

    return GuardedPrompt(
        original=original,
        normalized=normalized,
        accepted=True,
        reason="Mission prompt accepted as non-destructive assessment guidance.",
    )

