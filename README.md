# Lazy Hack 💤 - Fully Automating Cursor Lazily

This project runs Cursor autonomously using keyboard shortcuts and sound detection because we are **very lazy**.

## The *Even Lazier* Algorithm (Fully Automated)

1.  **Initial Prompt:** The script starts by asking Cursor to create `PRD.md` (requirements) and `status.md` (tasks).
2.  **Wait:** Listens for the AI completion sound.
3.  **Accept:** Sends `Cmd + Enter`.
4.  **New Tab:** Opens a new chat tab (`Ctrl + Cmd + T`).
5.  **Prompt "Proceed":** Types `let's proceed to build this app` and hits `Enter`.
6.  **Wait:** Listens for the AI completion sound.
7.  **Accept:** Sends `Cmd + Enter`.
8.  **New Tab:** Opens a new chat tab (`Ctrl + Cmd + T`).
9.  **Prompt "Summarize":** Types `summarize our state of work in status.md` and hits `Enter`.
10. **Loop:** Go back to step 2 and keep being lazy.

## How to Run (The Lazy Way)

1.  **Clone:** Get this repo.
2.  **Setup Env:**
    *   `python -m venv .venv`
    *   Activate it (e.g., `source .venv/bin/activate` or your `activate` alias).
    *   `pip install -r requirements.txt`
    *   *(Optional)* Create a `.env` file if you need to override sound detection defaults (see `auto_builder.py`).
3.  **Setup Cursor:**
    *   **IMPORTANT:** Open a *new, empty* Cursor window in a separate folder (e.g., `mkdir app && code app`). This keeps your project clean.
    *   Make sure Cursor is the **active, focused window**.
    *   Set these **Keyboard Shortcuts** in Cursor:
        *   `File: New Chat Tab` -> `Ctrl + Cmd + T`
        *   `Chat: Focus Input` -> `Cmd + L`
        *   *(Implied)* Accept changes likely uses `Cmd + Enter` by default.
4.  **Run the Bot:**
    *   In a terminal **outside** the `app` folder (i.e., in *this* `lazy-cursor` folder), run:
        `python auto_builder.py`
5.  **Watch & Be Lazy:** The script will take over the Cursor window in the `app` folder.

## Our Lazy Cursor Rules (Summary)

*   **TDD:** We try to follow Test-Driven Development.
*   **Secrets:** Use `.env` for secrets.
*   **Environment:** Always use a `.venv` created with `python -m venv .venv` and activate it.
*   **Project Definition:** `PRD.md` holds the project description.
*   **Project Status:** `status.md` tracks progress and next steps.
*   **Control:** The script reads `PRD.md` and `status.md` when told to "proceed".

Now go be lazy and let the script do the work! 