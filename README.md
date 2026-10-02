# Human vs Rule-Based AI

An educational Python/Streamlit app with two games:

- **Common-sense quiz:** answer eight multiple-choice questions, then compare your answers with a keyword chatbot. See scores, per-question explanations, and download results as CSV.
- **Guess the pattern:** enter the next number and your reasoning across six rounds. Compare with a script that recognizes only constant addition or multiplication.
- **Try the chatbot:** explore negation, rephrasing, and rule order using your own prompts.

This is a deliberately limited rule-based demonstration, not a trained AI model. The examples illustrate its specific rules and limitations, not human superiority over AI in general. Finite number sequences can have many valid continuations; scoring uses the stated intended rule. The app records reasoning but does not measure intuition.

## Run locally

Use Python 3.11 or newer. From the project folder:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the localhost address displayed in the terminal.

## Upload to GitHub and deploy

GitHub stores the source code. Run the Python web app on Streamlit Community Cloud; uploading to GitHub alone does not run it, and GitHub Pages does not execute a Python backend.

1. Extract the ZIP. Create a GitHub repository such as `common-sense-ai-games`.
2. Upload the **contents** of `common_sense_games` to the repository root. Ensure `app.py`, `game_logic.py`, and `requirements.txt` are alongside `README.md`, not inside another nested folder. Include `.github/workflows/tests.yml` if you want automated checks.
3. Sign in at https://share.streamlit.io and connect GitHub.
4. Choose **Create app**, select the repository and branch (usually `main`), and enter `app.py` as the main file path.
5. Choose Python 3.11 in advanced settings if offered, then deploy.
6. Share the resulting `.streamlit.app` URL. Commit future code changes to the selected GitHub branch to update the app.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

No API keys, database, or secrets are required. Each visitor has their own session state. Reloading or disconnecting can reset results; download the CSV to retain quiz results.

## Checks

```bash
python -m unittest discover -s tests -v
```

`game_logic.py` contains all questions, explanations, keyword rules, and pattern rules. Edit it to customize the games. The chatbot ignores negation deliberately, and its rules run in order. Pattern prediction abstains when neither supported rule fits.
"# mitweek2assignment" 
