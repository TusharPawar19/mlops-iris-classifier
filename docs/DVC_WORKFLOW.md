# DVC Workflow Summary

## Remote Configuration
Configured a local folder (`~/dvc-remote-storage`) to act as the default DVC remote storage to simulate a cloud backend.

## Data Update Cycle
For every dataset change, the following cycle was strictly followed:
1. `dvc add <file>`: Tracked the new data and updated the `.dvc` metafile.
2. `git add <file>.dvc`: Staged the DVC metafile in Git (tracking the pointer, not the data).
3. `git commit`: Recorded the data version in Git history.
4. `dvc push`: Uploaded the actual dataset to the remote storage.

## Version Comparison & Restoration
- `dvc diff <commit-hash>` was used to compare the dataset in a previous Git commit against the current workspace.
- `git checkout <commit-hash> -- <file>.dvc` combined with `dvc checkout` was used to switch the metafile pointer and restore the exact historical dataset version from the DVC cache.