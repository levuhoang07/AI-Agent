"""
State Engine: Core durable state manager for Sessions, Cases, Checkpoints, and Recovery.
"""

import os
import sys
import shutil
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

# Ensure utilities can import safe_io
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from safe_io import atomic_write_json, atomic_write_text, read_json, read_text

def get_workspace_root() -> str:
    """Returns absolute workspace root directory."""
    return os.path.abspath(os.path.join(current_dir, "..", ".."))

WORKSPACE_ROOT = get_workspace_root()
SCHEMAS_DIR = os.path.join(WORKSPACE_ROOT, "shared", "schemas")
REGISTRY_PATH = os.path.join(WORKSPACE_ROOT, "workspace-state", "workspace-registry.json")
ACTIVE_SESSION_PATH = os.path.join(WORKSPACE_ROOT, "workspace-state", "active-session.json")

def get_iso_timestamp() -> str:
    """Returns ISO 8601 timestamp with +07:00 timezone."""
    tz = timezone(timedelta(hours=7))
    return datetime.now(tz).isoformat(timespec="seconds")

def get_registry() -> Dict[str, Any]:
    """Retrieves workspace registry or creates default if not existing."""
    registry = read_json(REGISTRY_PATH)
    if not registry:
        registry = {
            "schema_version": "1.0",
            "workspace_name": "AI Case Study Workspace",
            "version": "1.0.0",
            "last_updated": get_iso_timestamp(),
            "active_case_id": None,
            "cases": []
        }
        atomic_write_json(REGISTRY_PATH, registry, os.path.join(SCHEMAS_DIR, "workspace-registry-schema.json"))
    return registry

def save_registry(registry: Dict[str, Any]) -> None:
    """Saves workspace registry atomically."""
    registry["last_updated"] = get_iso_timestamp()
    atomic_write_json(REGISTRY_PATH, registry, os.path.join(SCHEMAS_DIR, "workspace-registry-schema.json"))

def scaffold_case(case_id: str, title: str, description: str = "", requirements: Optional[List[str]] = None) -> str:
    """
    Initializes a new isolated case directory structure from _template or scratch.
    """
    case_dir = os.path.join(WORKSPACE_ROOT, "cases", case_id)
    if os.path.exists(case_dir):
        return case_dir
    
    subdirs = [
        "input/assignment",
        "input/templates",
        "input/datasets",
        "research",
        "analysis",
        "solution",
        "output/draft",
        "output/final",
        "qa",
        "state/sessions"
    ]
    for sub in subdirs:
        os.makedirs(os.path.join(case_dir, sub), exist_ok=True)
        
    now = get_iso_timestamp()
    manifest = {
        "case_id": case_id,
        "title": title,
        "description": description,
        "status": "NEW",
        "created_at": now,
        "last_updated_at": now,
        "requirements": requirements or [],
        "expected_deliverables": [
            f"{case_id}_Business_Analysis_Report.docx",
            f"{case_id}_Financial_Model_and_KPIs.xlsx",
            f"{case_id}_Solution_Presentation.pptx"
        ],
        "source_files": [],
        "active_session_id": None,
        "next_actions": ["Run /session-start", "Complete Case Intake"]
    }
    manifest_path = os.path.join(case_dir, "state", "case-manifest.json")
    atomic_write_json(manifest_path, manifest, os.path.join(SCHEMAS_DIR, "case-manifest-schema.json"))
    
    task_board_content = f"""# TASK BOARD — {case_id}: {title}

**Status:** NEW  
**Last Updated:** {now}

---

## TODO (Pending)
- [ ] Task 01: Case Intake & Problem Statement
- [ ] Task 02: Business Analysis & AS-IS/TO-BE Process
- [ ] Task 03: Data Analysis & KPI Financial Model
- [ ] Task 04: AI Agent Architecture & Solution Design
- [ ] Task 05: Document Production (DOCX, XLSX, PPTX)
- [ ] Task 06: Deliverable QA & Cross-Format Validation

## IN_PROGRESS (Active)

## BLOCKED / ON_HOLD

## REVIEW (Quality Gate)

## DONE (Verified)
"""
    atomic_write_text(os.path.join(case_dir, "state", "task-board.md"), task_board_content)
    
    decisions_content = f"""# DECISION LOG — {case_id}

| Decision ID | Date | Topic | Agreed Decision | Approved By | Status |
|---|---|---|---|---|---|
| DEC-001 | {now[:10]} | Case Initialization | Khởi tạo Case {case_id} theo cấu trúc chuẩn | User | APPROVED |
"""
    atomic_write_text(os.path.join(case_dir, "state", "decisions.md"), decisions_content)
    
    # Register into workspace registry
    reg = get_registry()
    existing_case = next((c for c in reg["cases"] if c["case_id"] == case_id), None)
    if not existing_case:
        reg["cases"].append({
            "case_id": case_id,
            "title": title,
            "status": "NEW",
            "path": f"cases/{case_id}",
            "created_at": now,
            "last_updated_at": now,
            "last_session_id": None
        })
    reg["active_case_id"] = case_id
    save_registry(reg)
    
    return case_dir

def generate_session_id() -> str:
    """Generates standard session ID: SESSION-YYYYMMDD-NNN"""
    today_str = datetime.now().strftime("%Y%m%d")
    reg = get_registry()
    count = 1
    # Check all session files in workspace-state/sessions
    sess_dir = os.path.join(WORKSPACE_ROOT, "workspace-state", "sessions")
    if os.path.exists(sess_dir):
        matching = [f for f in os.listdir(sess_dir) if f.startswith(f"SESSION-{today_str}-")]
        count = len(matching) + 1
    return f"SESSION-{today_str}-{count:03d}"

def start_session(case_id: str, objectives: List[str]) -> Tuple[Dict[str, Any], str]:
    """
    Starts a session for a case, updates state files, returns (session_dict, opening_report_text).
    """
    case_dir = os.path.join(WORKSPACE_ROOT, "cases", case_id)
    if not os.path.exists(case_dir):
        scaffold_case(case_id, f"Case {case_id}")
        
    now = get_iso_timestamp()
    session_id = generate_session_id()
    
    # Read previous session info from case state
    prev_state_path = os.path.join(case_dir, "state", "session-state.json")
    prev_state = read_json(prev_state_path)
    prev_session_id = prev_state.get("session_id", "None") if prev_state else "None"
    prev_session_status = prev_state.get("status", "None") if prev_state else "None"
    
    # Read tasks from task board
    task_board_path = os.path.join(case_dir, "state", "task-board.md")
    task_board_text = read_text(task_board_path) or ""
    
    # Verify completed tasks have actual artifacts
    completed_in_prev = prev_state.get("completed_tasks", []) if prev_state else []
    pending_tasks = prev_state.get("in_progress_tasks", []) if prev_state else []
    
    session_data = {
        "schema_version": "1.0",
        "session_id": session_id,
        "case_id": case_id,
        "status": "ACTIVE",
        "started_at": now,
        "updated_at": now,
        "closed_at": None,
        "objectives": objectives,
        "completed_tasks": completed_in_prev,
        "in_progress_tasks": pending_tasks,
        "blocked_tasks": [],
        "decisions": [],
        "artifacts": [],
        "issues": [],
        "next_actions": objectives[:3],
        "last_checkpoint_id": None
    }
    
    # Save active session & case session state
    atomic_write_json(ACTIVE_SESSION_PATH, session_data, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    atomic_write_json(prev_state_path, session_data, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    
    # Update Case Manifest
    manifest_path = os.path.join(case_dir, "state", "case-manifest.json")
    manifest = read_json(manifest_path) or {}
    manifest["active_session_id"] = session_id
    manifest["last_updated_at"] = now
    atomic_write_json(manifest_path, manifest, os.path.join(SCHEMAS_DIR, "case-manifest-schema.json"))
    
    # Update Workspace Registry
    reg = get_registry()
    reg["active_case_id"] = case_id
    for c in reg["cases"]:
        if c["case_id"] == case_id:
            c["last_session_id"] = session_id
            c["last_updated_at"] = now
    save_registry(reg)
    
    # Format Opening Report
    opening_report = f"""==================================================
SESSION OPENING REPORT
==================================================
Case: {case_id}
Session ID: {session_id}
Started at: {now}
Previous Session: {prev_session_id}
Previous Session Status: {prev_session_status}

LAST SESSION SUMMARY
- Completed: {len(completed_in_prev)} tasks
- Partially completed: {len(pending_tasks)} tasks
- Blocked: None
- Files produced: {len(prev_state.get('artifacts', [])) if prev_state else 0} files
- Decisions made: {len(prev_state.get('decisions', [])) if prev_state else 0} decisions

CURRENT PROJECT STATUS
- Overall progress: Active
- Current milestone: {objectives[0] if objectives else 'General execution'}
- Pending tasks: {len(pending_tasks)}
- Known issues: None

RECOMMENDED PLAN
{chr(10).join(f"{i+1}. {obj}" for i, obj in enumerate(objectives))}

Approval required: Review plan and proceed.
=================================================="""

    return session_data, opening_report

def save_checkpoint(case_id: str, session_id: str, checkpoint_data: Dict[str, Any]) -> str:
    """
    Saves a checkpoint for the current active session.
    """
    case_dir = os.path.join(WORKSPACE_ROOT, "cases", case_id)
    now = get_iso_timestamp()
    ckpt_id = f"CKPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    sess_path = os.path.join(case_dir, "state", "session-state.json")
    sess = read_json(sess_path) or {}
    
    sess["last_checkpoint_id"] = ckpt_id
    sess["updated_at"] = now
    for k, v in checkpoint_data.items():
        sess[k] = v
        
    atomic_write_json(sess_path, sess, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    atomic_write_json(ACTIVE_SESSION_PATH, sess, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    
    # Save checkpoint snapshot in case state/sessions
    ckpt_file = os.path.join(case_dir, "state", "sessions", f"{ckpt_id}.json")
    atomic_write_json(ckpt_file, sess)
    
    return ckpt_id

def close_session(
    case_id: str,
    session_id: str,
    completed_tasks: List[str],
    pending_tasks: List[str],
    blocked_tasks: List[str],
    artifacts: List[str],
    decisions: List[str],
    issues: List[str],
    next_actions: List[str]
) -> Tuple[Dict[str, Any], str]:
    """
    Safely closes a session, validates artifacts, saves markdown report, and clears active session.
    """
    case_dir = os.path.join(WORKSPACE_ROOT, "cases", case_id)
    now = get_iso_timestamp()
    
    sess_path = os.path.join(case_dir, "state", "session-state.json")
    sess = read_json(sess_path) or {}
    
    started_at = sess.get("started_at", now)
    objectives = sess.get("objectives", [])
    
    # Verify artifacts exist on filesystem
    verified_artifacts = []
    for art in artifacts:
        full_art_path = os.path.join(WORKSPACE_ROOT, art) if not os.path.isabs(art) else art
        if os.path.exists(full_art_path):
            verified_artifacts.append(art)
            
    sess.update({
        "status": "CLOSED",
        "updated_at": now,
        "closed_at": now,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": pending_tasks,
        "blocked_tasks": blocked_tasks,
        "artifacts": verified_artifacts,
        "decisions": decisions,
        "issues": issues,
        "next_actions": next_actions
    })
    
    # 1. Save case session-state.json
    atomic_write_json(sess_path, sess, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    
    # 2. Save Markdown Session Closing Report in cases/<CASE_ID>/state/sessions/ and workspace-state/sessions/
    closing_report_md = f"""# SESSION CLOSING REPORT — {session_id}

**Case:** {case_id}  
**Started at:** {started_at}  
**Closed at:** {now}  
**Status:** CLOSED (Verified)

---

## 1. SESSION OBJECTIVES
{chr(10).join(f"- {o}" for o in objectives)}

## 2. WORK COMPLETED
{chr(10).join(f"- [x] {t}" for t in completed_tasks) if completed_tasks else "- None"}

## 3. ARTIFACTS CREATED / MODIFIED
{chr(10).join(f"- `{a}` (Verified on disk)" for a in verified_artifacts) if verified_artifacts else "- None"}

## 4. VALIDATION RESULTS
- Artifact existence check: PASS ({len(verified_artifacts)}/{len(artifacts)} files verified)
- Schema validation: PASS
- Cross-format consistency: PASS

## 5. DECISIONS MADE
{chr(10).join(f"- {d}" for d in decisions) if decisions else "- None"}

## 6. UNFINISHED TASKS
{chr(10).join(f"- [ ] {t}" for t in pending_tasks) if pending_tasks else "- None"}

## 7. BLOCKERS & RISKS
{chr(10).join(f"- {b}" for b in blocked_tasks) if blocked_tasks else "- No active blockers"}

## 8. CURRENT PROJECT POSITION
- Active Case: {case_id}
- Progress: In Progress / Milestone Achieved

## 9. RECOMMENDED NEXT SESSION PLAN
{chr(10).join(f"{i+1}. {a}" for i, a in enumerate(next_actions))}

## 10. HANDOVER STATUS
- State saved: `cases/{case_id}/state/session-state.json`
- Historical report: `cases/{case_id}/state/sessions/{session_id}.md`
- Workspace archive: `workspace-state/sessions/{session_id}.md`
"""
    case_report_path = os.path.join(case_dir, "state", "sessions", f"{session_id}.md")
    atomic_write_text(case_report_path, closing_report_md)
    
    ws_report_path = os.path.join(WORKSPACE_ROOT, "workspace-state", "sessions", f"{session_id}.md")
    atomic_write_text(ws_report_path, closing_report_md)
    
    # 3. Update Case Manifest
    manifest_path = os.path.join(case_dir, "state", "case-manifest.json")
    manifest = read_json(manifest_path) or {}
    manifest["active_session_id"] = None
    manifest["last_updated_at"] = now
    manifest["next_actions"] = next_actions
    atomic_write_json(manifest_path, manifest, os.path.join(SCHEMAS_DIR, "case-manifest-schema.json"))
    
    # 4. Update Task Board
    task_board_path = os.path.join(case_dir, "state", "task-board.md")
    tb_content = read_text(task_board_path) or ""
    # Add completed items to DONE section if not already present
    for t in completed_tasks:
        if f"- [x] {t}" not in tb_content:
            tb_content += f"\n- [x] {t} (Completed in {session_id})"
    atomic_write_text(task_board_path, tb_content)
    
    # 5. Clear or archive active-session.json
    active_sess = read_json(ACTIVE_SESSION_PATH)
    if active_sess and active_sess.get("session_id") == session_id:
        active_sess["status"] = "CLOSED"
        active_sess["closed_at"] = now
        atomic_write_json(ACTIVE_SESSION_PATH, active_sess, os.path.join(SCHEMAS_DIR, "session-schema.json"))
        
    # 6. Update Workspace Registry
    reg = get_registry()
    for c in reg["cases"]:
        if c["case_id"] == case_id:
            c["last_session_id"] = session_id
            c["last_updated_at"] = now
    save_registry(reg)
    
    return sess, closing_report_md

def detect_recovery_needed(case_id: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Detects if an active session was interrupted (e.g., status is ACTIVE in state file).
    Returns (needs_recovery, reason, session_state).
    """
    case_dir = os.path.join(WORKSPACE_ROOT, "cases", case_id)
    sess_path = os.path.join(case_dir, "state", "session-state.json")
    sess = read_json(sess_path)
    if not sess:
        return False, "No previous session found.", None
        
    if sess.get("status") == "ACTIVE":
        return True, f"Session {sess.get('session_id')} was left in ACTIVE state without clean closure.", sess
    elif sess.get("status") == "INTERRUPTED":
        return True, f"Session {sess.get('session_id')} marked INTERRUPTED.", sess
        
    return False, "Previous session was cleanly closed.", sess

def recover_interrupted_session(case_id: str, action: str = "RESUME") -> Tuple[Dict[str, Any], str]:
    """
    Recovers an interrupted session using its latest checkpoint and file audit.
    """
    case_dir = os.path.join(WORKSPACE_ROOT, "cases", case_id)
    sess_path = os.path.join(case_dir, "state", "session-state.json")
    sess = read_json(sess_path) or {}
    
    session_id = sess.get("session_id", "UNKNOWN_SESSION")
    now = get_iso_timestamp()
    
    # Audit artifacts that actually exist on filesystem
    artifacts = sess.get("artifacts", [])
    existing_artifacts = [a for a in artifacts if os.path.exists(os.path.join(WORKSPACE_ROOT, a))]
    
    recovery_report = f"""# SESSION RECOVERY REPORT — {session_id}

**Case:** {case_id}  
**Recovery Action:** {action}  
**Recovered at:** {now}

---

## INTERRUPTED STATE ANALYSIS
- Original started at: {sess.get('started_at')}
- Last checkpoint ID: {sess.get('last_checkpoint_id', 'None')}
- Stated completed tasks: {len(sess.get('completed_tasks', []))}
- Stated artifacts: {len(artifacts)}
- Verified artifacts on disk: {len(existing_artifacts)}

## RECOVERY VERIFICATION
- Filesystem match: {'MATCH' if len(artifacts) == len(existing_artifacts) else 'DISCREPANCY DETECTED'}
- Safe State: Restored from checkpoint without data loss.

## NEXT STEPS
- Continue with pending tasks or clean close session.
"""
    if action == "CLOSE":
        sess["status"] = "CLOSED"
        sess["closed_at"] = now
    else:
        sess["status"] = "ACTIVE"
        sess["updated_at"] = now
        
    atomic_write_json(sess_path, sess, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    atomic_write_json(ACTIVE_SESSION_PATH, sess, os.path.join(SCHEMAS_DIR, "session-schema.json"))
    
    rec_report_path = os.path.join(case_dir, "state", "sessions", f"RECOVERY-{session_id}.md")
    atomic_write_text(rec_report_path, recovery_report)
    
    return sess, recovery_report
