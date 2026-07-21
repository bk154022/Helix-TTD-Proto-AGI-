import time
import json
import hashlib
from dataclasses import dataclass
from typing import Any, Optional


# ============================================================
# PHASE 7
# INTERFACE BOUNDARY ISOLATION
# CONSTITUTIONAL MIDDLEWARE
# ============================================================


# ============================================================
# CORE TEMPORAL PARAMETERS
# ============================================================

EPOCH_BUDGET_MS = 100

EPOCH_BUDGET_SECONDS = (
    EPOCH_BUDGET_MS / 1000.0
)


# ============================================================
# INTERFACE STATUS
# ============================================================

ACCEPTED = "ACCEPTED"

QUARANTINED = "QUARANTINED"

NULL_SINK = "NULL_SINK"


# ============================================================
# INGRESS PACKET
# ============================================================

@dataclass
class IngressPacket:

    source: str

    payload: Any

    epoch_timestamp: float

    packet_hash: str


# ============================================================
# PACKET HASH
# ============================================================

def calculate_packet_hash(
    source,
    payload,
    epoch_timestamp
):

    serialized_payload = json.dumps(

        {

            "source": source,

            "payload": payload,

            "epoch_timestamp": epoch_timestamp

        },

        sort_keys=True

    ).encode(

        "utf-8"

    )

    return hashlib.sha256(

        serialized_payload

    ).hexdigest()


# ============================================================
# PACKET CREATION
# ============================================================

def create_packet(
    source,
    payload
):

    epoch_timestamp = time.time()

    packet_hash = calculate_packet_hash(

        source,

        payload,

        epoch_timestamp

    )

    return IngressPacket(

        source=source,

        payload=payload,

        epoch_timestamp=epoch_timestamp,

        packet_hash=packet_hash

    )


# ============================================================
# INTERFACE BOUNDARY
# ============================================================

class InterfaceBoundary:

    def __init__(
        self,

        epoch_budget_seconds=EPOCH_BUDGET_SECONDS
    ):

        self.epoch_budget_seconds = (

            epoch_budget_seconds

        )


    def validate_packet(
        self,

        packet: IngressPacket
    ):

        current_time = time.time()

        packet_age = (

            current_time

            - packet.epoch_timestamp

        )


        # ----------------------------------------------------
        # TEMPORAL VALIDATION
        # ----------------------------------------------------

        if (

            packet_age

            > self.epoch_budget_seconds

        ):

            return {

                "status": QUARANTINED,

                "sink": NULL_SINK,

                "reason": (

                    "Packet exceeded "

                    "epoch time budget."

                ),

                "packet_age_seconds": packet_age

            }


        # ----------------------------------------------------
        # PACKET INTEGRITY VALIDATION
        # ----------------------------------------------------

        expected_hash = (

            calculate_packet_hash(

                packet.source,

                packet.payload,

                packet.epoch_timestamp

            )

        )


        if packet.packet_hash != expected_hash:

            return {

                "status": QUARANTINED,

                "sink": NULL_SINK,

                "reason": (

                    "Packet integrity "

                    "verification failed."

                ),

                "packet_age_seconds": packet_age

            }


        # ----------------------------------------------------
        # ACCEPTED PACKET
        # ----------------------------------------------------

        return {

            "status": ACCEPTED,

            "sink": None,

            "reason": (

                "Packet passed interface "

                "boundary validation."

            ),

            "packet_age_seconds": packet_age,

            "payload": packet.payload

        }


# ============================================================
# NULL SINK
# ============================================================

class NullSink:

    @staticmethod
    def discard(packet):

        return {

            "status": NULL_SINK,

            "discarded": True,

            "source": packet.source

        }


# ============================================================
# INTERFACE RUNTIME
# ============================================================

def process_packet(

    boundary,

    packet

):

    result = boundary.validate_packet(

        packet

    )


    if result["status"] == ACCEPTED:

        print(

            "[ACCEPTED] "

            "Packet passed interface boundary."

        )

        return result


    print(

        "[QUARANTINE] "

        "Packet rejected by interface boundary."

    )


    print(

        "[NULL SINK] "

        "External packet isolated."

    )


    sink_result = NullSink.discard(

        packet

    )


    return {

        **result,

        **sink_result

    }


# ============================================================
# VALIDATION TESTS
# ============================================================

def test_valid_packet():

    print(

        "\n[TEST 1] Valid Packet"

    )

    boundary = InterfaceBoundary()

    packet = create_packet(

        source="sensor",

        payload={

            "temperature": 25.4,

            "status": "normal"

        }

    )

    result = process_packet(

        boundary,

        packet

    )

    assert (

        result["status"]

        == ACCEPTED

    )

    print(

        "[PASS] Valid packet accepted."

    )


def test_expired_packet():

    print(

        "\n[TEST 2] Expired Packet"

    )

    boundary = InterfaceBoundary()

    packet = create_packet(

        source="sensor",

        payload={

            "temperature": 25.4,

            "status": "delayed"

        }

    )

    # Artificially age the packet
    packet.epoch_timestamp -= (

        EPOCH_BUDGET_SECONDS

        + 1.0

    )

    result = process_packet(

        boundary,

        packet

    )

    assert (

        result["status"]

        == NULL_SINK

    )

    print(

        "[PASS] Expired packet isolated."

    )


def test_tampered_packet():

    print(

        "\n[TEST 3] Tampered Packet"

    )

    boundary = InterfaceBoundary()

    packet = create_packet(

        source="software_integrity_verifier",

        payload={

            "package": "helix-runtime",

            "version": "2.1.1"

        }

    )

    # Modify payload after hash creation
    packet.payload["version"] = "tampered"

    result = process_packet(

        boundary,

        packet

    )

    assert (

        result["status"]

        == NULL_SINK

    )

    print(

        "[PASS] Tampered packet isolated."


    )


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():

    print("=" * 60)

    print(

        "PHASE 7 : INTERFACE BOUNDARY ISOLATION"

    )

    print(

        "CONSTITUTIONAL MIDDLEWARE"

    )

    print("=" * 60)


    print(

        "\nEpoch Budget:"

    )

    print(

        f"  {EPOCH_BUDGET_MS} ms"

    )


    test_valid_packet()

    test_expired_packet()

    test_tampered_packet()


    print("\n" + "=" * 60)

    print(

        "[SUCCESS] Interface boundary validation completed."

    )

    print(

        "[SUCCESS] Temporal isolation verified."

    )

    print(

        "[SUCCESS] Integrity isolation verified."

    )

    print(

        "[SUCCESS] Null sink quarantine verified."

    )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()