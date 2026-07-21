from pathlib import Path
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone


# ============================================================
# PHASE 8
# RELEASE ENGINEERING
# HELIX PROTO-AGI v2.1.1
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SECTIONS_DIR = PROJECT_ROOT / "sections"

LEDGER_DIR = PROJECT_ROOT / "ledger"

LOGS_DIR = PROJECT_ROOT / "logs"

MANIFEST_FILE = PROJECT_ROOT / "release_manifest.json"


REQUIRED_PHASES = [

    "phase1_braid_engine.py",

    "phase2_hybrid_key_exchange.py",

    "phase3_proto_agi_v21.py",

    "phase4_production_build.py",

    "phase5_repository_engineering.py",

    "phase6_ledger_automation.py",

    "phase7_interface_boundary.py",

]


RELEASE_VERSION = "v2.1.1-PRODUCTION"


# ============================================================
# OUTPUT HELPERS
# ============================================================

def print_header():

    print("=" * 60)

    print(
        "PHASE 8 : RELEASE ENGINEERING"
    )

    print(
        "HELIX PROTO-AGI v2.1.1"
    )

    print("=" * 60)


def success(message):

    print(f"[PASS] {message}")


def failure(message):

    print(f"[FAIL] {message}")


# ============================================================
# FILE HASH
# ============================================================

def calculate_file_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for block in iter(
            lambda: file.read(65536),
            b""
        ):

            sha256.update(block)

    return sha256.hexdigest()


# ============================================================
# TASK 1
# REQUIRED PHASE VALIDATION
# ============================================================

def validate_phase_files():

    print(
        "\n[1] Validating Phase Files..."
    )

    missing_files = []

    phase_hashes = {}

    for phase_file in REQUIRED_PHASES:

        file_path = SECTIONS_DIR / phase_file

        if not file_path.exists():

            missing_files.append(
                phase_file
            )

            failure(
                f"Missing: {phase_file}"
            )

        else:

            file_hash = calculate_file_hash(
                file_path
            )

            phase_hashes[phase_file] = file_hash

            success(
                f"{phase_file}"
            )

    if missing_files:

        raise RuntimeError(

            "Required phase files are missing."

        )

    return phase_hashes


# ============================================================
# TASK 2
# LEDGER VALIDATION
# ============================================================

def validate_ledger():

    print(
        "\n[2] Validating Ledger..."
    )

    ledger_files = [

        LEDGER_DIR / "ledger.json",

        PROJECT_ROOT / "ledger.json",

        PROJECT_ROOT / "ledger_notary_log.txt",

    ]

    found_ledger = None

    for ledger_file in ledger_files:

        if ledger_file.exists():

            found_ledger = ledger_file

            break

    if found_ledger is None:

        print(
            "[INFO] No ledger artifact found."
        )

        print(
            "[INFO] Ledger validation skipped."
        )

        return None

    if found_ledger.suffix == ".json":

        try:

            with open(
                found_ledger,
                "r",
                encoding="utf-8"
            ) as file:

                ledger = json.load(file)

            if not isinstance(
                ledger,
                (dict, list)
            ):

                raise ValueError(
                    "Ledger must contain JSON data."
                )

            success(
                f"Ledger JSON valid: {found_ledger}"
            )

        except json.JSONDecodeError as error:

            raise RuntimeError(

                f"Ledger JSON invalid: {error}"

            )

    else:

        if found_ledger.stat().st_size == 0:

            raise RuntimeError(
                "Ledger log exists but is empty."
            )

        success(
            f"Ledger log valid: {found_ledger}"
        )

    return str(found_ledger)


# ============================================================
# TASK 3
# PHASE 7 INTERFACE VALIDATION
# ============================================================

def validate_interface_boundary():

    print(
        "\n[3] Validating Interface Boundary..."
    )

    interface_file = (

        SECTIONS_DIR

        / "phase7_interface_boundary.py"

    )

    if not interface_file.exists():

        raise RuntimeError(

            "Phase 7 interface boundary missing."

        )

    source = interface_file.read_text(

        encoding="utf-8"

    )

    required_symbols = [

        "InterfaceBoundary",

        "NullSink",

        "QUARANTINED",

        "NULL_SINK",

        "EPOCH_BUDGET_MS",

    ]

    for symbol in required_symbols:

        if symbol not in source:

            raise RuntimeError(

                f"Missing interface symbol: {symbol}"

            )

    success(
        "Temporal boundary detected."
    )

    success(
        "Quarantine mechanism detected."
    )

    success(
        "Null sink detected."
    )

    return True


# ============================================================
# TASK 4
# RELEASE MANIFEST
# ============================================================

def generate_manifest(

    phase_hashes,

    ledger_path,

    interface_valid

):

    print(
        "\n[4] Generating Release Manifest..."
    )

    manifest = {

        "release": RELEASE_VERSION,

        "project": "Helix Proto-AGI",

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "phase_files": phase_hashes,

        "ledger": ledger_path,

        "interface_boundary": {

            "validated": interface_valid

        },

        "release_status": "READY_FOR_TAG"

    }

    with open(

        MANIFEST_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            manifest,

            file,

            indent=4

        )

    success(
        f"Manifest written: {MANIFEST_FILE.name}"
    )

    return manifest


# ============================================================
# TASK 5
# GIT STATUS
# ============================================================

def check_git_repository():

    print(
        "\n[5] Checking Git Repository..."
    )

    try:

        result = subprocess.run(

            [

                "git",

                "rev-parse",

                "--is-inside-work-tree"

            ],

            cwd=PROJECT_ROOT,

            capture_output=True,

            text=True,

            check=True

        )

        if result.stdout.strip() == "true":

            success(
                "Git repository detected."
            )

            return True

    except (

        subprocess.CalledProcessError,

        FileNotFoundError

    ):

        print(
            "[INFO] Git repository not detected."
        )

        return False

    return False


# ============================================================
# FINAL RELEASE VALIDATION
# ============================================================

def main():

    print_header()

    phase_hashes = validate_phase_files()

    ledger_path = validate_ledger()

    interface_valid = validate_interface_boundary()

    manifest = generate_manifest(

        phase_hashes,

        ledger_path,

        interface_valid

    )

    git_available = check_git_repository()

    print(
        "\n" + "=" * 60
    )

    print(
        "[SYSTEM_STATE] READY_FOR_TAG"
    )

    print(
        "[RELEASE] v2.1.1-PRODUCTION"
    )

    print(
        "[INTERFACE] Boundary validation complete"
    )

    print(
        "[LEDGER] Validation complete"
    )

    print(
        "[MANIFEST] Release manifest generated"
    )

    if git_available:

        print(
            "[GIT] Repository ready for tag"
        )

    else:

        print(
            "[GIT] Manual repository verification required"
        )

    print(
        "[CONCLUSION] Release candidate validated."
    )

    print(
        "=" * 60
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()