# Fix: Replace broken a-i-skills directory with proper git clone

## Context

The local directory `/Users/4jp/world/realm/operate/org/liminal/repo/a-i-skills` is **not a git repository**. It has no `.git` directory and no remote configured. The git commands that appear to work are actually resolving to a home-level repo at `/Users/4jp/.git`, which is unrelated.

This is the only repo in the `liminal/repo/` directory with this problem — all 8 siblings are proper clones. The remote at `organvm-iv-taxis/a-i--skills` has 10+ commits (Platinum Sprint, Silver Sprint, CI, ADRs, etc.) that are absent locally.

Additionally, `~/Workspace/a-i--skills` is a symlink → `…/liminal/repo/a-i-skills`, so it's also affected.

## Steps

### 1. Remove the broken directory
```bash
rm -rf /Users/4jp/world/realm/operate/org/liminal/repo/a-i-skills
```

### 2. Clone the remote repo into the correct location
Clone using the local directory name (`a-i-skills`, single dash) to preserve the existing symlink:
```bash
gh repo clone organvm-iv-taxis/a-i--skills /Users/4jp/world/realm/operate/org/liminal/repo/a-i-skills
```

### 3. Verify
- Confirm `git remote -v` shows the GitHub remote
- Confirm `git log --oneline` matches the remote history (latest: `0511963 chore: add seed.yaml`)
- Confirm `~/Workspace/a-i--skills` symlink still resolves correctly

## Files affected
- `/Users/4jp/world/realm/operate/org/liminal/repo/a-i-skills/` — deleted and replaced
- `~/Workspace/a-i--skills` — symlink, unchanged (still points to same path)
