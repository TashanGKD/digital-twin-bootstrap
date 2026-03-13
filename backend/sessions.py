"""会话管理：内存会话 + profiles 目录自动落盘 + 量表数据"""
import uuid
import json
from datetime import date
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent  # digital-twin-bootstrap/
PROFILES_DIR = REPO_ROOT / "profiles"
TEMPLATE_PATH = REPO_ROOT / "profiles" / "_template.md"
PROFILE_TITLE_PREFIX = "# 科研人员画像 — "
PLACEHOLDER_IDENTIFIERS = {"[姓名/标识]", "姓名/标识"}


def _load_template() -> str:
    today_str = date.today().strftime("%Y-%m-%d")
    return TEMPLATE_PATH.read_text(encoding="utf-8").replace("YYYY-MM-DD", today_str)


def _today_unnamed() -> str:
    return f"unnamed-{date.today().strftime('%Y-%m-%d')}"


def _sanitize_identifier(identifier: str) -> str:
    cleaned = identifier.strip()
    if cleaned in PLACEHOLDER_IDENTIFIERS or not cleaned:
        return _today_unnamed()
    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or _today_unnamed()


def _extract_profile_identifier(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(PROFILE_TITLE_PREFIX):
            return _sanitize_identifier(stripped[len(PROFILE_TITLE_PREFIX):])
        if stripped.startswith("# "):
            return _sanitize_identifier(stripped[2:])
        break
    return _today_unnamed()


def _normalize_existing_path(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    return Path(path_value)


def _session_suffix(session: dict) -> str:
    sid = session.get("session_id") or ""
    if sid:
        return sid.replace("-", "")[:8]
    return uuid.uuid4().hex[:8]


def _target_profile_path(content: str, session: dict) -> Path:
    identifier = _extract_profile_identifier(content)
    suffix = _session_suffix(session)
    return PROFILES_DIR / f"{identifier}-{suffix}.md"


def _relocate_file_if_needed(current_path: Path | None, target_path: Path) -> None:
    if not current_path or current_path == target_path or not current_path.exists():
        return
    if target_path.exists():
        current_path.unlink()
        return
    current_path.rename(target_path)


def save_profile(session: dict, content: str) -> Path:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    target_path = _target_profile_path(content, session)
    current_path = _normalize_existing_path(session.get("profile_path"))
    _relocate_file_if_needed(current_path, target_path)
    target_path.write_text(content, encoding="utf-8")
    session["profile"] = content
    session["profile_path"] = str(target_path)
    forum_content = session.get("forum_profile", "")
    if forum_content:
        forum_target_path = _target_forum_profile_path(session)
        forum_current_path = _normalize_existing_path(session.get("forum_profile_path"))
        _relocate_file_if_needed(forum_current_path, forum_target_path)
        forum_target_path.write_text(forum_content, encoding="utf-8")
        session["forum_profile_path"] = str(forum_target_path)
    return target_path


def _target_forum_profile_path(session: dict) -> Path:
    profile_path = _normalize_existing_path(session.get("profile_path"))
    if not profile_path:
        profile_path = _target_profile_path(session.get("profile", ""), session)
    return profile_path.with_name(f"{profile_path.stem}-论坛画像.md")


def save_forum_profile(session: dict, content: str) -> Path:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    profile_content = session.get("profile", "")
    if profile_content:
        save_profile(session, profile_content)
    target_path = _target_forum_profile_path(session)
    current_path = _normalize_existing_path(session.get("forum_profile_path"))
    _relocate_file_if_needed(current_path, target_path)
    target_path.write_text(content, encoding="utf-8")
    session["forum_profile"] = content
    session["forum_profile_path"] = str(target_path)
    return target_path


def save_scales(session: dict, scale_name: str, data: dict) -> None:
    """保存量表结果到会话 + 落盘 JSON"""
    if "scales" not in session:
        session["scales"] = {}
    data["completed_at"] = date.today().strftime("%Y-%m-%d")
    session["scales"][scale_name] = data

    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    profile_path = _normalize_existing_path(session.get("profile_path"))
    if profile_path:
        scales_path = profile_path.with_suffix(".scales.json")
    else:
        suffix = _session_suffix(session)
        scales_path = PROFILES_DIR / f"scales-{suffix}.json"
    scales_path.write_text(
        json.dumps(session["scales"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


_sessions: dict[str, dict] = {}


def get_or_create(session_id: str | None = None) -> tuple[str, dict]:
    if session_id and session_id in _sessions:
        s = _sessions[session_id]
        s.setdefault("session_id", session_id)
        s.setdefault("forum_profile", "")
        s.setdefault("profile_path", None)
        s.setdefault("forum_profile_path", None)
        s.setdefault("scales", {})
        return session_id, s
    sid = session_id or str(uuid.uuid4())
    _sessions[sid] = {
        "session_id": sid,
        "messages": [],
        "profile": _load_template(),
        "forum_profile": "",
        "profile_path": None,
        "forum_profile_path": None,
        "scales": {},
    }
    return sid, _sessions[sid]


def get(session_id: str) -> dict | None:
    return _sessions.get(session_id)


def reset(session_id: str) -> dict:
    _sessions[session_id] = {
        "session_id": session_id,
        "messages": [],
        "profile": _load_template(),
        "forum_profile": "",
        "profile_path": None,
        "forum_profile_path": None,
        "scales": {},
    }
    return _sessions[session_id]
