# Jozi Buddy: project steering

## Project
"Jozi Buddy" is a local voice AI agent: a politically neutral
voting-information assistant for South Africa's 2026 local government
elections (4 November 2026). It asks the user about their priorities,
then compares their answers to party manifestos.

## Stack
- Python 3.12 in `.venv`, on a Windows laptop with microphone and speakers
- Strands Bidi Agents (GA imports: `strands.bidi.agent.BidiAgent`,
  `strands.bidi.io.AudioIO`, `strands.bidi.models.BedrockNovaSonicModel`)
- Amazon Nova Sonic: model id `amazon.nova-2-5-sonic`, region `us-east-1`
  (fallback: `amazon.nova-2-sonic-v1:0`)
- Use `AudioIO(audio_processor=True)` for echo cancellation
- Voice: `tiffany`. English only (Nova Sonic does not support SA languages yet)

## Structure
- `voice_agent.py`: the BidiAgent, system prompt, audio I/O
- `tools.py`: `list_topics`, `get_positions`, `score_alignment`
- `data/topics.json`: fixed list of topic IDs
- `data/positions.json`: party x topic positions with manifesto page numbers
- `scripts/extract_pages.py`: builds page-tagged text from the PDFs
- `docs/index.html`: GitHub Pages landing page

## Behaviour rules
- Never tell the user who to vote for. Never give an opinion on any party.
- Treat every party identically: same questions, same depth, same tone.
- Only describe party positions from `data/positions.json` via tools.
  Do not use outside knowledge about party positions.
- Always name the party and the manifesto page when stating a position.
- If a manifesto is silent on a topic, say "no stated position".
- Separate a party's own commitments from its criticism of rivals.
- Describe manifesto promises as promises, not as track record.
- Spoken replies: one or two short sentences.
- RISE Mzansi's document is the 2024 national manifesto. Say so when used.
- For voting stations and dates, point the user to the IEC.

## Security
- Never hardcode, print or log AWS keys. Use the default AWS profile.
- Never read or open `Secrete code.txt`, `.env` or `~/.aws/credentials`.
- Never commit secrets, `.venv/`, PDFs or `build/`. Check `git status`
  before every push.

## Working style
- Keep code simple and commented for a beginner.
- Verify Strands Bidi APIs against the installed package before using them.
- Test with text and a few spoken checks before adding features.