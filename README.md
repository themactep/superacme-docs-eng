# SuperAcme docs (English symlink view)

This repository provides an English-named view of the SuperAcme documentation by creating symlinks to the original repository, included as a git submodule at `superacme-src/`.

- Filenames and directories are best-effort translated to English; abbreviations are preserved.
- Symlinks point into the submodule. No large binaries are duplicated here.
- As translations are produced, symlinks can be replaced by real translated files.

Submodule setup:
- The submodule URL is the original repo URL if available; otherwise, a relative local path is used.

## Quick start (Linux/macOS)

Copy and run these commands:

```bash
# Clone this repo and pull submodules in one step
git clone --recurse-submodules https://github.com/themactep/superacme-docs-eng.git
cd superacme-docs-eng

# Ensure submodules are initialized (safe to re-run)
git submodule update --init --recursive
```

You can browse the English-named tree under `acme_doc_release/` immediately. No large files are duplicated here; they live inside the `superacme-src/` submodule.

Regenerate symlinks (only needed if you update the submodule or want to refresh names):

```bash
# Create a local venv and install pypinyin for transliteration
python3 -m venv .venv
source .venv/bin/activate
pip install pypinyin

# Rebuild the English-named symlink tree pointing into the submodule
python _tools/generate_english_symlinks.py --src superacme-src --dest . --prefix acme_doc_release
```

## Updating to latest docs

```bash
# Pull latest repo and submodules
git pull --recurse-submodules
git submodule update --init --recursive

# (Optional) Regenerate the English symlinks after submodule updates
python _tools/generate_english_symlinks.py --src superacme-src --dest . --prefix acme_doc_release
```

## Windows notes

- Enable “Developer Mode” or run your shell as Administrator to allow symlink creation.
- Use the Python launcher (`py -3`) if `python` points to Python 2 or is missing.

```powershell
# Clone with submodules
git clone --recurse-submodules https://github.com/themactep/superacme-docs-eng.git
cd superacme-docs-eng

git submodule update --init --recursive

# Create venv and install pypinyin
py -3 -m venv .venv
.venv\Scripts\activate
pip install pypinyin

# Regenerate symlinks
py -3 _tools\generate_english_symlinks.py --src superacme-src --dest . --prefix acme_doc_release
```

## Troubleshooting

- Submodule access: the submodule points to `http://27.188.56.209:8088/superacme/acme_doc_release.git`. You may need network/VPN access and credentials to fetch it.
- Symlink issues on Windows: ensure you have symlink privileges (Developer Mode or Administrator). If symlinks fail, you can still access original content inside `superacme-src/` directly.
