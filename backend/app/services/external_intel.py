import json
from urllib import error, request

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.monitoring import ExternalIntelReport


BLOCKED_QUERY_TERMS = {
    "password",
    "api key",
    "secret",
    "token",
    "exploit",
    "bypass",
    "credential",
}


def run_external_intel_search(db: Session, query: str) -> ExternalIntelReport:
    normalized_query = " ".join(query.strip().split())
    lower_query = normalized_query.lower()
    blocked_term = next((term for term in BLOCKED_QUERY_TERMS if term in lower_query), None)

    if blocked_term:
        return ExternalIntelReport(
            query=normalized_query,
            source="serper",
            status="rejected",
            summary=f"External intelligence request rejected because it included blocked term: {blocked_term}.",
            evidence="Prompt guard blocked the request before any external API call.",
        )

    if not settings.serper_api_key:
        return ExternalIntelReport(
            query=normalized_query,
            source="serper",
            status="not_configured",
            summary="SERPER_API_KEY is not configured, so no external intelligence search was performed.",
            evidence="Add SERPER_API_KEY to .env and restart the backend to enable public search intelligence.",
        )

    results = _call_serper(normalized_query)
    summary = _summarise_results(normalized_query, results)
    return _save_report(
        db,
        query=normalized_query,
        status="completed",
        summary=summary,
        evidence=json.dumps(results[:5], indent=2),
    )


def get_external_intel_status(db: Session) -> dict:
    latest = (
        db.query(ExternalIntelReport)
        .filter(ExternalIntelReport.status == "completed")
        .order_by(ExternalIntelReport.created_at.desc())
        .first()
    )
    return {
        "connected": bool(settings.serper_api_key),
        "status": "connected" if settings.serper_api_key else "not_configured",
        "latest_summary": latest.summary if latest else None,
    }


def _call_serper(query: str) -> list[dict]:
    payload = json.dumps({"q": query, "num": 5}).encode("utf-8")
    req = request.Request(
        "https://google.serper.dev/search",
        data=payload,
        headers={
            "X-API-KEY": settings.serper_api_key or "",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        return [{"title": "Serper request failed", "snippet": str(exc), "link": ""}]

    return data.get("organic", [])


def _summarise_results(query: str, results: list[dict]) -> str:
    if not results:
        return f"No public search results were returned for: {query}."

    titles = [item.get("title", "Untitled result") for item in results[:3]]
    return f"External public intelligence for '{query}' returned {len(results)} results. Top signals: {'; '.join(titles)}."


def _save_report(db: Session, query: str, status: str, summary: str, evidence: str) -> ExternalIntelReport:
    report = ExternalIntelReport(
        query=query,
        source="serper",
        status=status,
        summary=summary,
        evidence=evidence,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
