#!/usr/bin/env bash
# Refresh the participant repo (github.com/MajedTuah/4Hour_Session) from student/.
#   ./publish_student.sh [path-to-4Hour_Session-clone]      default: ~/Repos/4Hour_Session
# Rebuilds the notebooks, copies the current deck into student/slides/, then mirrors student/ into the clone.
# Solutions (student_solutions/) are never published. Review, commit and push in the clone yourself.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-$HOME/Repos/4Hour_Session}"

if [ ! -d "$TARGET/.git" ]; then
  echo "✖ $TARGET is not a git clone. Run: git clone https://github.com/MajedTuah/4Hour_Session.git \"$TARGET\""
  exit 1
fi

python3 "$HERE/student_build/build_notebooks.py"

mkdir -p "$HERE/student/slides/assets"
cp "$HERE/index.html" "$HERE/student/slides/index.html"
cp "$HERE"/assets/*.png "$HERE/student/slides/assets/"

rsync -a --delete \
  --exclude ".git/" --exclude ".venv/" --exclude "__pycache__/" --exclude ".ipynb_checkpoints/" \
  --exclude "artifacts/" --exclude "mlruns/" --exclude "reports/" --exclude ".DS_Store" \
  "$HERE/student/" "$TARGET/"

echo
echo "✔ Synced into $TARGET"
git -C "$TARGET" status --short
echo
echo "Review, then:  cd \"$TARGET\" && git add -A && git commit -m \"Update Day 1 materials\" && git push"
