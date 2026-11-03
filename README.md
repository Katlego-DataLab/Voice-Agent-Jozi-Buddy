<div align="center">

# Jozi Buddy

### A politically neutral voice assistant for South Africa's 2026 local government elections

Talk to it. Ask what each party says about the issues you care about. It tells you, with the manifesto page, and **never tells you who to vote for**.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Strands Agents](https://img.shields.io/badge/Strands-Bidi%20Agents-6C47FF?style=for-the-badge)
![Amazon Nova Sonic](https://img.shields.io/badge/Amazon-Nova%20Sonic-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon Bedrock](https://img.shields.io/badge/AWS-Bedrock-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Kiro](https://img.shields.io/badge/Built%20with-Kiro%20IDE-8A2BE2?style=for-the-badge)
![Rich](https://img.shields.io/badge/Terminal-Rich-00A86B?style=for-the-badge)
![Neutral](https://img.shields.io/badge/Stance-Politically%20Neutral-2E8B57?style=for-the-badge)
![Election](https://img.shields.io/badge/SA%20Local%20Elections-4%20Nov%202026-DE3831?style=for-the-badge)

</div>

---

##  Table of contents

- [What is Jozi Buddy?](#-what-is-jozi-buddy)
- [Neutrality promise](#-neutrality-promise)
- [What you can ask](#-what-you-can-ask)
- [How it works](#-how-it-works)
- [What the project requires](#-what-the-project-requires)
- [Setup](#-setup)
- [Run it](#-run-it)
- [Project structure](#-project-structure)
- [Data sources](#-data-sources)
- [Method](#-method)
- [Limitations](#-limitations)
- [Make it your own](#-make-it-your-own)
- [Voting information](#-voting-information)

---

##  What is Jozi Buddy?

Party manifestos are long, dense and hard to compare. **Jozi Buddy** is a real-time voice agent that listens through your microphone and answers through your speakers. You tell it what matters to you, such as water, electricity, jobs or crime, and it explains what each of six parties says it will do, with the manifesto page so you can check for yourself.

It shows live captions in the terminal: a status line (Listening, Thinking, Speaking), Jozi Buddy's words appearing as it speaks, and your own words under "You".

## Neutrality promise

- It **never recommends a party** and never says who to vote for. If asked, it politely declines and offers a comparison instead.
- It treats every party with the **same tone and length**.
- It only describes positions from the reference data, **always naming the party and the page**.
- If a party has no dedicated commitment on a topic, it says so instead of guessing.
- It describes what parties **say they will do**, not whether it will work or what they have done in the past.

## What you can ask

- "I care about jobs and safety. What does each party say about those?"
- "What does the DA say about water?"
- "Compare the ANC and ActionSA on corruption."
- "What does VF Plus say about healthcare?" *(it will say there is no dedicated commitment)*
- "What does RISE Mzansi say about land?" *(it will note this is the 2024 national manifesto)*
- "Who should I vote for?" *(it will decline and offer a comparison)*

##  How it works

```
 You speak ──► Microphone ──► Strands BidiAgent ──► Amazon Nova Sonic (Bedrock)
                                    │                       │
                         system prompt + rules              │
                         + data/positions.md                ▼
 Live captions (Rich) ◄──── transcript events ◄──── Spoken reply ──► Speakers
```

1. **Audio in and out:** Strands `AudioIO` captures your microphone and plays the reply, with echo cancellation so laptop speakers work.
2. **Speech to speech:** Amazon Nova Sonic on Amazon Bedrock listens and talks back in near real time. You can interrupt it mid-sentence.
3. **Grounding:** the contents of `data/positions.md` are loaded into the system prompt as reference data. The agent is instructed to answer only from it.
4. **Rules:** the system prompt sets the neutrality rules, the citation rules, and short spoken replies of two sentences.
5. **Captions:** the `rich` library draws the banner, spinner and live transcript in the terminal.

##  What the project requires

**Accounts**
- An **AWS account** with Amazon Bedrock available in `us-east-1`.
- A **GitHub account** (to publish or clone the repo).

**Tools**
- **Python 3.12** (the Nova Sonic model class in Strands requires 3.12 or newer, and 3.12 has prebuilt PyAudio wheels on Windows).
- **git**.
- **Kiro IDE** (optional, used to build the project).
- A working **microphone and speakers or headphones**. Headphones give the cleanest experience.

**AWS setup**
1. In the AWS Console, open **Amazon Bedrock**, set the region to **us-east-1**, go to **Model access**, and enable **Amazon Nova Sonic**. Note the exact model ID shown.
2. Create an IAM user for the project with permission to use Bedrock, then create an access key.
3. Save the credentials in `~/.aws/credentials` (on Windows, `C:\Users\YOUR_USERNAME\.aws\credentials`):

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

and the region in `~/.aws/config`:

```ini
[default]
region = us-east-1
output = json
```

>  **Never commit credentials.** They live outside the project folder, and `.gitignore` also blocks `.aws/` and `.env`.

**Python packages** (see `requirements.txt`)
- `strands-agents[bidi-all,bidi-pyaudio]` for the agent, the Nova Sonic model and microphone/speaker audio.
- `rich` for the live terminal captions.

**Data**
- `data/positions.md`: the party comparison the agent answers from.

## Setup

```powershell
# 1. Clone
git clone https://github.com/Katlego-DataLab/Voice-Agent-Jozi-Buddy.git
cd Voice-Agent-Jozi-Buddy

# 2. Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
```

On macOS or Linux, use `python3 -m venv .venv` and `source .venv/bin/activate`.

Then check your AWS credentials work:

```powershell
python -c "import boto3; print(boto3.client('sts').get_caller_identity()['Arn'])"
```

##  Run it

```powershell
python voice_agent.py
```

Wait for "Listening", then say hello. Press **Ctrl+C** to end the conversation.

**Troubleshooting**
- **Cuts itself off:** use headphones and make sure no other app is using the microphone.
- **No sound:** check your operating system's default output device.
- **Credentials or access errors:** confirm Nova Sonic is enabled in Bedrock for `us-east-1`.
- **Data not found:** `data/positions.md` must exist in the project folder.

##  Project structure

```
Voice-Agent-Jozi-Buddy/
├── voice_agent.py        # The voice agent, system prompt and live captions
├── data/
│   └── positions.md      # Party comparison the agent answers from
├── requirements.txt      # Python dependencies
├── .kiro/steering/       # Project context for the Kiro IDE
├── .gitignore            # Keeps secrets and large files out of git
└── README.md
```

## Data sources

Six party manifestos were compared:

| Party | Document |
| --- | --- |
| ActionSA | ActionSA Manifesto 2026 |
| ANC | ANC Local Government Manifesto 2026 |
| DA | DA Local Government Manifesto 2026, "Getting South Africa Working for All" |
| EFF | EFF Local Government Manifesto 2026 |
| RISE Mzansi | People's Manifesto, 20 January 2024 (**national**, not local) |
| VF Plus | VF Plus Manifesto 2026, "It Is Time" |

Topics covered: water, electricity, infrastructure and service delivery, jobs and economic growth, corruption and governance, crime and safety, land reform and transformation, healthcare, and education.

##  Method

- Each party was summarised **topic by topic with the same approach**, using only what its manifesto says.
- Every line carries its **page reference**. These are **PDF page numbers**. They match the printed numbers for five documents, but the **EFF's printed numbers are 2 lower** than the PDF pages.
- Where a party has no dedicated commitment, the data says so.
- Summaries were drafted with AI assistance from the manifesto text and should be **checked against the original documents**.

##  Limitations

- **English only.** Nova Sonic does not yet support South Africa's official languages other than English, so words like *eish* or *sawubona* may sound off.
- **Promises, not track record.** It describes what parties say they will do, not what they have delivered.
- **RISE Mzansi is a 2024 national manifesto**, so its commitments are not local-government specific.
- **Education and healthcare** are mostly provincial functions, so local manifestos say little about them.
- The summaries may contain errors. Always check the original manifestos.
- It is an information tool, not advice. It does not predict election results.

## Make it your own

- Edit `SYSTEM_PROMPT` in `voice_agent.py` to change the personality or the rules.
- Replace `data/positions.md` to cover other topics, parties or countries.
- Change the `voice` setting on the model to try a different Nova Sonic voice.

## Voting information

For official details on where, when and how to vote, visit the **Electoral Commission of South Africa (IEC)**: [elections.org.za](https://www.elections.org.za).

---

<div align="center">

**Built with love 🤍 by Katlego Mathebula**

</div>
