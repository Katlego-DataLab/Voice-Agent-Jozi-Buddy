"""voice_agent.py — Jozi Voice Buddy

Entry point for the Jozi Buddy voice assistant.
Run with:  python voice_agent.py
Press Ctrl+C to stop.
"""

import asyncio
import logging
from pathlib import Path

from strands.bidi.agent import BidiAgent
from strands.bidi.io import AudioIO
from strands.bidi.models import BedrockNovaSonicModel

# ---------------------------------------------------------------------------
# Logging — INFO level so you can see what the agent is doing without noise
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Reference data — load data/positions.md at startup (UTF-8)
# The file must exist before running; see scripts/extract_pages.py to build it.
# ---------------------------------------------------------------------------
_POSITIONS_PATH = Path(__file__).parent / "data" / "positions.md"

try:
    _positions_text = _POSITIONS_PATH.read_text(encoding="utf-8")
    logger.info("Loaded reference data from %s (%d chars)", _POSITIONS_PATH, len(_positions_text))
except FileNotFoundError:
    # Fail loudly so the agent never runs without its reference data
    raise FileNotFoundError(
        f"Reference data not found at {_POSITIONS_PATH}. "
        "Run scripts/extract_pages.py to generate it before starting the agent."
    )

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
_BASE_PROMPT = """
You are Jozi Buddy, a politically neutral voting-information assistant for
South Africa's 2026 local government elections (4 November 2026).

RULES — follow these strictly in every reply:

1. REFERENCE DATA ONLY — Only describe party positions using the reference
   data appended below. Never use outside knowledge about any party.

2. CITATIONS — Always name the party and the manifesto page number when
   stating a position (e.g. "The ANC promises X — page 12").

3. NO STATED POSITION — If the reference data shows a party has no dedicated
   commitment on a topic, say "[Party] has no stated position on that topic."

4. RISE MZANSI — RISE Mzansi's commitments come from its 2024 national
   manifesto (not a 2026 local-election document), so say so each time you
   reference it.

5. NEVER RECOMMEND — Never say who the user should vote for. If asked,
   politely decline and offer to compare parties on the topics they care about.

6. PARITY — Treat every party with the same tone and the same level of detail.
   Do not volunteer criticism or praise for any party.

7. SPOKEN BREVITY — Keep every reply to two short sentences, then ask which
   topic or party the user wants to explore next.

8. IEC REFERRAL — For voting station locations, registration, or election
   dates, direct the user to the IEC at www.elections.org.za.
""".strip()

# Append the reference data under a clear heading
SYSTEM_PROMPT = (
    _BASE_PROMPT
    + "\n\n---\n\n## REFERENCE DATA\n\n"
    + _positions_text
)

# ---------------------------------------------------------------------------
# Model — Nova Sonic 2.5, us-east-1, voice tiffany
# Credentials come from the default AWS profile; never hardcode keys here.
# ---------------------------------------------------------------------------
model = BedrockNovaSonicModel(
    model_id="amazon.nova-2-5-sonic",
    region="us-east-1",
    voice="tiffany",
)

# ---------------------------------------------------------------------------
# Audio I/O — audio_processor=True enables echo cancellation so the mic
# does not pick up the speaker output.
# Requires:  pip install "strands-agents[bidi-aec]"
# ---------------------------------------------------------------------------
audio_io = AudioIO(audio_processor=True)

# ---------------------------------------------------------------------------
# Agent — built after positions.md is loaded so SYSTEM_PROMPT is complete
# ---------------------------------------------------------------------------
agent = BidiAgent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main() -> None:
    """Start Jozi Buddy and run until the user presses Ctrl+C."""
    logger.info("Jozi Buddy starting — speak into your microphone. Press Ctrl+C to stop.")
    try:
        await agent.run(
            inputs=[audio_io.input()],
            outputs=[audio_io.output()],
        )
    except KeyboardInterrupt:
        logger.info("Stopped by user.")


if __name__ == "__main__":
    asyncio.run(main())
