import os
import json
import hashlib
from datetime import datetime

# ============================================================
# PHASE 6
# LEDGER NOTARY AUTOMATION
# ============================================================

# Import validated production functions from Phase 4
from phase4_production_build import (
    VERIFIED_MATRIX,
    verify_root,
    generate_seed,
    generate_receipt,
    deterministic_mlkem_keygen
)


# ============================================================
# LEDGER CONFIGURATION
# ============================================================

LEDGER_DIR = "ledger"

LEDGER_FILE = os.path.join(
    LEDGER_DIR,
    "ledger.json"
)

INDEX_FILE = os.path.join(
    LEDGER_DIR,
    "ledger_index.json"
)


# ============================================================
# LEDGER INITIALIZATION
# ============================================================

def initialize_ledger():
    """
    Initialize the ledger directory and JSON files.

    Automatically repairs:
        - Missing ledger directory
        - Missing ledger.json
        - Empty ledger.json
        - Missing ledger_index.json
        - Empty ledger_index.json
    """

    os.makedirs(
        LEDGER_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Initialize or repair ledger.json
    # --------------------------------------------------------

    if (
        not os.path.exists(LEDGER_FILE)
        or os.path.getsize(LEDGER_FILE) == 0
    ):

        with open(
            LEDGER_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

    # --------------------------------------------------------
    # Initialize or repair ledger_index.json
    # --------------------------------------------------------

    if (
        not os.path.exists(INDEX_FILE)
        or os.path.getsize(INDEX_FILE) == 0
    ):

        initial_index = {

            "entries": 0,

            "latest_receipt": "",

            "latest_timestamp": "",

            "latest_version": "v2.1.1"

        }

        with open(
            INDEX_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                initial_index,
                file,
                indent=4
            )


# ============================================================
# LEDGER ENTRY CREATION
# ============================================================

def append_ledger(
    trace,
    seed,
    receipt
):
    """
    Append a new execution record to the ledger.

    The record contains:

        - Timestamp
        - Version
        - Trace value
        - Trace magnitude
        - SHA-512 topological seed
        - SHA-256 receipt
        - Verification hash
    """

    # --------------------------------------------------------
    # Generate UTC timestamp
    # --------------------------------------------------------

    timestamp = (
        datetime.utcnow()
        .isoformat()
        + "Z"
    )

    # --------------------------------------------------------
    # Generate verification hash
    # --------------------------------------------------------

    verification_hash = hashlib.sha256(

        seed
        + receipt.encode(
            "utf-8"
        )

    ).hexdigest()

    # --------------------------------------------------------
    # Construct immutable execution record
    # --------------------------------------------------------

    record = {

        "timestamp": timestamp,

        "version": "v2.1.1",

        "trace_real": float(
            trace.real
        ),

        "trace_imag": float(
            trace.imag
        ),

        "trace_magnitude": float(
            abs(trace)
        ),

        "seed_sha512": seed.hex(),

        "receipt_sha256": receipt,

        "verification_hash": verification_hash

    }

    # --------------------------------------------------------
    # Safely load existing ledger
    # --------------------------------------------------------

    try:

        with open(
            LEDGER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            ledger = json.load(file)

        # Ledger must be a list
        if not isinstance(
            ledger,
            list
        ):

            ledger = []

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        # Recover from missing or corrupted JSON
        ledger = []

    # --------------------------------------------------------
    # Append new record
    # --------------------------------------------------------

    ledger.append(
        record
    )

    # --------------------------------------------------------
    # Save updated ledger
    # --------------------------------------------------------

    with open(
        LEDGER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            ledger,
            file,
            indent=4
        )

    # --------------------------------------------------------
    # Update ledger index
    # --------------------------------------------------------

    index = {

        "entries": len(
            ledger
        ),

        "latest_receipt": receipt,

        "latest_timestamp": timestamp,

        "latest_version": "v2.1.1"

    }

    with open(
        INDEX_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            index,
            file,
            indent=4
        )

    return verification_hash


# ============================================================
# PHASE 6 EXECUTION
# ============================================================

def main():

    print("=" * 60)

    print(
        "PHASE 6 : LEDGER AUTOMATION"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # 1. Initialize ledger
    # --------------------------------------------------------

    print(
        "\n[0] Initializing ledger..."
    )

    initialize_ledger()

    print(
        "[OK] Ledger initialized."
    )

    # --------------------------------------------------------
    # 2. Verify topological root
    # --------------------------------------------------------

    print(
        "\n[1] Verifying Root..."
    )

    trace = verify_root(
        VERIFIED_MATRIX
    )

    # --------------------------------------------------------
    # 3. Generate topological seed
    # --------------------------------------------------------

    print(
        "\n[2] Generating Topological Seed..."
    )

    seed = generate_seed(
        trace
    )

    # --------------------------------------------------------
    # 4. Generate sovereign receipt
    # --------------------------------------------------------

    print(
        "\n[3] Generating Receipt..."
    )

    receipt = generate_receipt(
        seed
    )

    # --------------------------------------------------------
    # 5. Generate deterministic ML-KEM material
    # --------------------------------------------------------

    print(
        "\n[4] Deterministic ML-KEM Key Generation..."
    )

    pk, sk = deterministic_mlkem_keygen(
        seed
    )

    # --------------------------------------------------------
    # 6. Append ledger entry
    # --------------------------------------------------------

    print(
        "\n[5] Writing immutable ledger entry..."
    )

    verification_hash = append_ledger(

        trace,

        seed,

        receipt

    )

    print(
        "[OK] Ledger updated successfully."
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n" + "=" * 60
    )

    print(
        "PHASE 6 LEDGER SUMMARY"
    )

    print(
        "=" * 60
    )

    print(
        "\nTrace Magnitude:"
    )

    print(
        f"  {abs(trace):.12f}"
    )

    print(
        "\nTopological Seed SHA-512:"
    )

    print(
        f"  {seed.hex()}"
    )

    print(
        "\nSovereign Receipt SHA-256:"
    )

    print(
        f"  {receipt}"
    )

    print(
        "\nVerification Hash SHA-256:"
    )

    print(
        f"  {verification_hash}"
    )

    print(
        "\nPublic Key:"
    )

    print(
        f"  {pk}"
    )

    print(
        "\nPrivate Key:"
    )

    print(
        f"  {sk}"
    )

    print(
        "\nLedger File:"
    )

    print(
        f"  {LEDGER_FILE}"
    )

    print(
        "\nLedger Index:"
    )

    print(
        f"  {INDEX_FILE}"
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "[SUCCESS] Ledger automation completed."
    )

    print(
        "[SUCCESS] Execution record appended."
    )

    print(
        "[SUCCESS] Ledger index synchronized."
    )

    print(
        "=" * 60
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()