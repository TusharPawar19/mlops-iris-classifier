Verification & Execution Steps
1.	dvc --version returns a valid 3.x version string.
2.	ls .dvc/cache (or dvc cache dir) shows populated cache directories containing hashed data objects after dvc add.
3.	git log --oneline -- data/raw/iris_v1.csv.dvc shows exactly 2 commits, confirming two tracked dataset versions.
4.	dvc diff a1b2c3d (using your actual first commit hash) reports data/raw/iris_v1.csv as Modified.
5.	ls ~/dvc-remote-storage (the local remote) contains hashed object subdirectories after dvc push, confirming data was uploaded to the remote independently of Git.
6.	After dvc checkout to the older .dvc pointer, wc -l data/raw/iris_v1.csv reports 151 lines; after switching back, it reports 171 lines — confirming DVC correctly restores each historical data version on demand.
7.	docs/DVC_WORKFLOW.md exists and accurately documents the remote and workflow used.
DVC Remote Storage structure
C:\Users\Admin\dvc-remote-storage
│
└── files
    │
    └── md5
        │
        ├── 21
        │   └── d441a28bce4417276097df955afc50
        │
        └── 67
            └── 4c8c36bb7c4ba8d851dee9e6ee67af

What are those two files?
Those long names are MD5 content hashes.
They are not random filenames. DVC essentially does:
iris_v1.csv
     ↓
calculate MD5 hash
     ↓
21d441a28bce4417276097df955afc50
     ↓
store it as:
files/md5/21/d441a28bce4417276097df955afc50
The first two characters become the folder name:
21 / d441a28bce4417276097df955afc50
Similarly:
67 / 4c8c36bb7c4ba8d851dee9e6ee67af
And the really interesting part...
You have two hashes, which strongly indicates that DVC has stored two different versions/objects.
Most likely:
Version 1
150 rows
     ↓
hash → 21d441a28bce4417276097df955afc50

Version 2
170 rows
     ↓
hash → 674c8c36bb7c4ba8d851dee9e6ee67af
