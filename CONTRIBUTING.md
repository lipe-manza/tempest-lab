# Contributing

Start from the base named by the maintainer for your change. The project uses `dev` for development. Check the remote before assuming `master` is current. The local branch `testing/pre-sdr-release` contains the release review work. A clone only includes committed changes available from its remote.

## Start a focused change

```sh
git clone https://github.com/lipe-manza/gr-tempest.git
cd gr-tempest
git fetch origin
git branch -a
git switch -c docs/test-instructions origin/dev
```

Fetch updates remote references without replacing working files. Before updating a feature branch, check `git status`. Commit work you intend to keep. To set unfinished work aside, use `git stash push -u`. This includes untracked files and leaves ignored files behind. Review `git stash list` and use `git stash apply` to recover the changes while keeping a copy.

## Review and commit

```sh
git status --short
git diff -- docs/BUILD_QA.md
git add -- docs/BUILD_QA.md
git diff --cached --check
git diff --cached
git commit -m "docs: explain how to interpret offline test results"
git show --stat HEAD
```

Stage specific files. Keep build trees, installation prefixes, recordings, datasets, credentials, and local logs outside the staged diff. Use `git restore --staged -- PATH` to unstage a file while preserving its contents. The working-tree form `git restore -- PATH` discards unstaged edits.

## Submit and update a pull request

Run the tests relevant to your change as described in [docs/BUILD_QA.md](docs/BUILD_QA.md). Report the exact revision, platform, command, exit code, expected result and actual result. Use a small synthetic fixture for bug reports.

Verify the push destination with `git remote get-url --push origin`. If it belongs to the intended fork, publish the feature branch with `git push -u origin docs/test-instructions`. Open a pull request against the agreed base. Link the issue and attach a redacted test summary. Public CI, when configured, supplements the local checks.

To bring updated base changes into a clean feature branch, fetch and run `git merge origin/dev` on that feature branch. For conflicts, inspect `git status`, resolve each marked section, stage only the resolved files, and run the tests before completing the merge. Use `git merge --abort` to abandon an in-progress merge started from a clean tree. Add review fixes as ordinary commits on the same branch and push again to update the pull request.
