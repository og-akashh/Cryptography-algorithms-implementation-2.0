# Cryptography Algorithms Implementation: Secure Message Encryption and Decryption Using Python

> **Educational project.** This tool was built for learning during a one-month
> cybersecurity internship at Codec Technologies. It is **not** a complete enterprise
> encryption solution and has not been security-audited. See [Security limitations](#20-security-limitations).

## Table of contents

1. [Project overview](#1-project-overview)
2. [Problem statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Features](#4-features)
5. [Technologies used](#5-technologies-used)
6. [Basic cryptography concepts](#6-basic-cryptography-concepts)
7. [Encryption versus hashing](#7-encryption-versus-hashing)
8. [Symmetric versus asymmetric encryption](#8-symmetric-versus-asymmetric-encryption)
9. [Why Fernet was selected](#9-why-fernet-was-selected)
10. [Architecture and project structure](#10-architecture-and-project-structure)
11. [Installation on Windows](#11-installation-on-windows)
12. [Installation on Linux and macOS](#12-installation-on-linux-and-macos)
13. [Running the application](#13-running-the-application)
14. [Command examples](#14-command-examples)
15. [Complete sample workflow](#15-complete-sample-workflow)
16. [Running the automated tests](#16-running-the-automated-tests)
17. [Expected results](#17-expected-results)
18. [Verification status](#18-verification-status)
19. [Using the interactive menu](#19-using-the-interactive-menu)
20. [Security limitations](#20-security-limitations)
21. [Common errors and troubleshooting](#21-common-errors-and-troubleshooting)
22. [Publishing on GitHub](#22-publishing-on-github)
23. [Learning outcomes](#23-learning-outcomes)
24. [Future improvements](#24-future-improvements)
25. [Project author](#25-project-author)
26. [Disclaimer](#26-disclaimer)

---

## 1. Project overview

A command-line Python application that encrypts and decrypts text messages and UTF-8
text files using **Fernet** (authenticated symmetric encryption) from the Python
[`cryptography`](https://cryptography.io/) library. It offers both a beginner-friendly
interactive menu and scriptable commands with proper exit codes.

No custom cryptographic algorithm is implemented. All cryptography is delegated to a
well-reviewed library.

## 2. Problem statement

Plain-text messages and files can be read by anyone who gets access to them. Beginners
often try to "invent" their own ciphers, which are almost always insecure. This project
shows how to protect text **correctly**: by using a trusted library, managing keys
carefully, and handling errors safely.

## 3. Objectives

- Encrypt and decrypt text messages with a secret key.
- Generate and store keys safely, separately from ciphertext.
- Encrypt and decrypt text files without damaging the originals.
- Fail safely on wrong keys, corrupted data, or tampered data.
- Follow professional practices: tests, documentation, version control, CI.

## 4. Features

- Secure key generation (`Fernet.generate_key()`), saved with owner-only permissions where supported.
- Message encryption and decryption.
- File encryption and decryption (atomic writes, original never modified).
- Refusal to overwrite existing keys or files unless explicitly authorized.
- Friendly error messages (no stack traces for ordinary users) and non-zero exit codes.
- Interactive menu **and** direct commands.
- Automated test suite and GitHub Actions workflow.

## 5. Technologies used

| Technology | Purpose |
|---|---|
| Python 3.10+ (3.11 or 3.12 recommended) | Programming language |
| `cryptography` (Fernet) | Authenticated symmetric encryption |
| `argparse` | Command-line arguments |
| `pathlib` | Cross-platform file paths |
| `logging` | Diagnostic messages (never secrets) |
| `pytest` | Automated testing |
| `ruff` | Linting |
| Git and GitHub, GitHub Actions | Version control, publishing, automated checks |

## 6. Basic cryptography concepts

- **Plaintext**: the readable message. **Ciphertext**: the scrambled, protected form.
- **Key**: a secret value that controls encryption and decryption.
- **Encryption** turns plaintext into ciphertext; **decryption** reverses it with the right key.
- **Authenticated encryption** also detects whether the ciphertext was modified.

For simple explanations with examples, read [docs/CRYPTOGRAPHY_BASICS.md](docs/CRYPTOGRAPHY_BASICS.md).

## 7. Encryption versus hashing

| | Encryption | Hashing |
|---|---|---|
| Reversible? | Yes, with the key | No (one-way) |
| Uses a key? | Yes | Usually no |
| Purpose | Confidentiality | Fingerprints, integrity checks, password storage (with special algorithms) |
| Example here | Fernet | Not used for protecting messages |

Hashing is **not** a substitute for encryption. This project does not use MD5 or SHA-1.

## 8. Symmetric versus asymmetric encryption

- **Symmetric**: one shared secret key encrypts and decrypts (this project, Fernet). It is fast, but the key must be shared safely.
- **Asymmetric**: a public key encrypts and a private key decrypts (for example RSA). It helps with key exchange but is slower and more complex.

Fernet is symmetric only. It has no public-key features and no non-repudiation (it cannot prove *who* created a message, because everyone with the key can create valid tokens).

## 9. Why Fernet was selected

- It is a **high-level recipe** in a widely used library, so beginners cannot easily pick unsafe settings.
- It provides **confidentiality and integrity/authenticity**: tampered data is rejected.
- Keys are generated securely with a single function call.
- It is easy to explain: AES-128-CBC for encryption plus HMAC-SHA256 for authentication, with a random IV per message.

## 10. Architecture and project structure

```
python-cryptography-project/
├── main.py                  # Entry point (python main.py ...)
├── src/crypto_app/
│   ├── core.py              # Encrypt/decrypt text (no file or CLI code)
│   ├── key_manager.py       # Generate, save, load keys
│   ├── file_operations.py   # Safe file encryption/decryption, atomic writes
│   ├── cli.py               # argparse commands and interactive menu
│   └── exceptions.py        # Custom, safe error types
├── tests/                   # pytest test suite
├── docs/                    # Report, basics, usage, security design, presentation
├── examples/message.txt     # Sample file to encrypt
└── .github/workflows/tests.yml   # Automated tests on GitHub
```

```
cli.py  ──►  key_manager.py ──►  core.py
   │                │
   └──► file_operations.py ──►  core.py
```

Cryptography (`core.py`) is separated from the user interface (`cli.py`).

## 11. Installation on Windows

Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/) (tick **"Add python.exe to PATH"**). Then open **PowerShell** in the project folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and try again, or use Command Prompt with `.venv\Scripts\activate.bat`.

## 12. Installation on Linux and macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

A **virtual environment** (`.venv`) keeps this project's packages separate from the rest of your computer. Activate it every time you open a new terminal. `pip install -e .` is optional for running `python main.py`, but it also adds a `crypto-app` command.

## 13. Running the application

From the repository root:

```bash
python main.py            # starts the interactive menu
python main.py --help     # lists all commands
python main.py --version
```

(Use `python3` instead of `python` if your system requires it.)

## 14. Command examples

Messages typed on the command line can be saved in your shell history. For truly sensitive text, prefer the interactive menu.
On Windows PowerShell, always use **double quotes** around values.

**Generate a key** (refuses to replace an existing key; add `--force` to replace it deliberately):

```bash
python main.py generate-key --key-file keys/secret.key
```

**Encrypt a message** (prints only the ciphertext):

```bash
python main.py encrypt --key-file keys/secret.key --message "Hello World"
```

**Decrypt a message:**

```bash
python main.py decrypt --key-file keys/secret.key --token "PASTE_CIPHERTEXT_HERE"
```

**Encrypt a file** (original untouched; refuses to overwrite unless `--overwrite` is given):

```bash
python main.py encrypt-file --key-file keys/secret.key --input-file examples/message.txt --output-file output/encrypted.txt
```

**Decrypt a file:**

```bash
python main.py decrypt-file --key-file keys/secret.key --input-file output/encrypted.txt --output-file output/decrypted.txt
```

**Exit codes:** `0` success · `1` operation failed (wrong key, missing file, refused overwrite…) · `2` invalid arguments · `130` interrupted with Ctrl+C.

## 15. Complete sample workflow

**Linux/macOS (bash):**

```bash
# 1. Install dependencies (see sections 11-12)
# 2. Generate a key
python main.py generate-key --key-file keys/secret.key

# 3-4. Encrypt a message and keep the ciphertext
TOKEN=$(python main.py encrypt --key-file keys/secret.key --message "Hello World")
echo "$TOKEN"

# 5-6. Decrypt it with the same key; the output should be: Hello World
python main.py decrypt --key-file keys/secret.key --token "$TOKEN"

# 7. Try a different key: decryption must fail safely (exit code 1)
python main.py generate-key --key-file keys/wrong.key
python main.py decrypt --key-file keys/wrong.key --token "$TOKEN"
echo "Exit code: $?"

# 8. Encrypt a sample file
python main.py encrypt-file --key-file keys/secret.key --input-file examples/message.txt --output-file output/encrypted.txt

# 9. Decrypt the file, then compare with the original (no output from diff = identical)
python main.py decrypt-file --key-file keys/secret.key --input-file output/encrypted.txt --output-file output/decrypted.txt
diff examples/message.txt output/decrypted.txt

# 10. Run the automated tests
pytest

# 11. Publish on GitHub (see section 22)
```

**Windows PowerShell:** the same commands work, with these differences:

```powershell
$TOKEN = python main.py encrypt --key-file keys/secret.key --message "Hello World"
python main.py decrypt --key-file keys/secret.key --token "$TOKEN"
python main.py decrypt --key-file keys/wrong.key --token "$TOKEN"; echo "Exit code: $LASTEXITCODE"
fc.exe /b examples\message.txt output\decrypted.txt     # compare files
```

## 16. Running the automated tests

```bash
pytest          # run everything
pytest -v       # verbose: shows each test name
ruff check .    # lint check (also run by GitHub Actions)
```

The tests use temporary folders and freshly generated throwaway keys. They need no network access and never touch your real keys or files.

## 17. Expected results

- `pytest` ends with a green summary and **no failures**.
- `ruff check .` prints `All checks passed!`.
- In the workflow above: step 6 prints `Hello World`; step 7 prints `Error: Decryption failed...` and exit code `1`; step 9's `diff` prints nothing.
- Encrypting twice gives different ciphertexts (Fernet uses a random IV). This is normal.

## 18. Verification status

Honest status of what was checked while developing this project:

| Item | Status |
|---|---|
| Source code, sample workflow (all 11 steps' commands except publishing), exit codes, menu | Run and checked on Linux (Python 3.12) |
| Test suite (90 test cases) | All passed in the development environment, **using a small pytest-compatible runner** because `pytest` could not be installed offline there. |
| Real `pytest` run | **Please run `pytest` yourself** and confirm (step 10). |
| `ruff check .` | Configured, not executed in the development environment. Line lengths were checked manually. |
| Windows and macOS | Designed to be portable; not run by the author of this scaffold. The GitHub Actions workflow tests all three after you push. |
| GitHub publishing | Not done; you do this with the commands in section 22. |

## 19. Using the interactive menu

```
========================================
CRYPTOGRAPHY PROJECT
========================================

1. Generate a new encryption key
2. Encrypt a message
3. Decrypt a message
4. Encrypt a text file
5. Decrypt a text file
6. View help
7. Exit

Select an option:
```

Invalid choices are rejected and you are asked again. Errors are shown as friendly messages and the menu keeps running. You are asked before an existing key or output file is replaced.

## 20. Security limitations

- **Anyone with the key can decrypt.** Keep it secret and back it up. **If you lose the key, the data cannot be recovered.**
- Storing the key **next to** the ciphertext defeats the purpose if both are exposed together.
- Encryption does **not** protect a compromised computer (malware, keyloggers).
- Fernet gives confidentiality and integrity/authenticity, but **does not hide metadata**: approximate message length and the token creation time are visible.
- Fernet is symmetric only: no public-key encryption and no non-repudiation.
- Fernet works on data **held in memory**; it is not suitable for very large files (this tool limits files to 10 MiB).
- Filesystem permissions are **platform-dependent**. On Linux/macOS the key file is set to owner-only (`600`). On Windows, access control depends on NTFS folder permissions; keep keys inside your user profile.
- Wrong keys and tampered ciphertext produce the **same** error, because Fernet cannot tell them apart.
- No password-based keys, key rotation, or secure memory wiping is implemented.

Details: [docs/SECURITY_DESIGN.md](docs/SECURITY_DESIGN.md).

## 21. Common errors and troubleshooting

| Problem | Solution |
|---|---|
| `python` not found | Try `python3` (Linux/macOS) or `py` (Windows). Reinstall Python with "Add to PATH". |
| `ModuleNotFoundError: cryptography` | Activate the virtual environment and run `pip install -r requirements-dev.txt`. |
| PowerShell blocks `Activate.ps1` | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, or use `activate.bat` in Command Prompt. |
| `Key file not found` | Run `generate-key` first, or check the `--key-file` path. |
| `already exists and will not be overwritten` | Choose a new output name, or add `--overwrite` (files) / `--force` (keys) if you really mean it. |
| `Decryption failed` | Wrong key, or ciphertext was copied incompletely/modified. Copy the **entire** token. |
| `not a valid UTF-8 text file` | Only plain text files are supported (not images, PDFs, Word files). |
| Strange characters or `UnicodeEncodeError` on Windows | Set `PYTHONUTF8=1` (or run `chcp 65001`) before running. |
| `pytest` not found | Activate the virtual environment, or run `python -m pytest`. |
| `git push` rejected | See section 22; do not force-push unless you understand why. |

## 22. Publishing on GitHub

**Suggested repository name:** `python-cryptography-project`
**Suggested description:** *Beginner-friendly Python CLI for secure message and file encryption using Fernet, with tests, CI, and security documentation.*
**Suggested topics:** `python`, `cryptography`, `fernet`, `encryption`, `decryption`, `cybersecurity`, `cli`, `pytest`, `internship-project`, `education`

### What belongs in the repository, and what stays private

| Commit to GitHub | Keep private (already in `.gitignore`) |
|---|---|
| Source code in `src/` and `main.py` | `keys/` and any `*.key` file |
| `tests/`, `docs/`, `examples/message.txt` | `output/` (generated encrypted/decrypted files) |
| README, LICENSE, requirements, config, CI workflow | `.venv/`, `__pycache__/`, `.pytest_cache/`, `.env` files |

### Option A: Git command line

1. Create an **empty** repository on github.com (no README, no .gitignore, no license) named `python-cryptography-project`.
2. In the project folder:

```bash
git init
git branch -M main
git add .
git status          # CHECK: no keys/ or *.key files must appear in this list!
git commit -m "feat: initial commit - Fernet message and file encryption CLI"
git remote add origin https://github.com/<your-username>/python-cryptography-project.git
git push -u origin main
```

Replace `<your-username>` with your own GitHub username. GitHub asks you to sign in through your browser or the Git credential manager. **Never put a password or personal access token inside a command.**

### Option B: GitHub website (no Git commands)

1. Create a new repository on github.com.
2. Click **uploading an existing file**.
3. Drag in the project files and folders (**not** `keys/`, `output/`, or `.venv/`). The hidden folder `.github` must be included for the workflow; if your file manager hides it, enable "show hidden files".
4. Click **Commit changes**.

### Suggested commit messages for later changes

```
feat: add <new feature>
fix: handle <problem> in <module>
docs: update usage guide
test: add tests for <behaviour>
refactor: simplify <module>
chore: update dependencies
```

After pushing, open the **Actions** tab to see the tests run.

## 23. Learning outcomes

- Difference between encryption, hashing, and encoding.
- Symmetric vs asymmetric cryptography; authenticated encryption.
- Why you use trusted libraries instead of inventing algorithms.
- Safe key handling and the limits of encryption.
- Python packaging (src layout), `argparse`, `pathlib`, exceptions, and logging.
- Writing automated tests; using Git, GitHub, and CI.

## 24. Future improvements

- Password-derived keys using a proper KDF (Scrypt/PBKDF2/Argon2) with random salts.
- Key rotation with `MultiFernet`.
- Streaming/chunked encryption for large files.
- Public-key features and digital signatures for non-repudiation.
- Reading messages from standard input to avoid shell history.
- Optional GUI.

## 25. Project author

- **Name:** [YOUR NAME]
- **Enrollment number:** [ENROLLMENT NUMBER]
- **College:** [COLLEGE NAME]
- **Internship:** Codec Technologies, [START DATE] to [END DATE]
- **Supervisor:** [SUPERVISOR NAME]

## 26. Disclaimer

This project is for **educational purposes only**. It is **not** a complete enterprise encryption solution, has not been independently audited, and comes with no warranty. Do not rely on it to protect critical, regulated, or highly sensitive information.
