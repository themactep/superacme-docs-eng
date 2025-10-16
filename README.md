# SuperAcme docs (English symlink view)

This repository provides an English-named view of the SuperAcme documentation by creating symlinks to the original repository, included as a git submodule at .

- Filenames and directories are best-effort translated to English; abbreviations are preserved.
- Symlinks point into the submodule. No large binaries are duplicated here.
- As translations are produced, symlinks can be replaced by real translated files.

Submodule setup:
- The submodule URL is the original repo URL if available; otherwise, a relative local path is used.
