Running stage 'collect':
> python src/pipeline/collect.py --output data/raw/iris_raw.csv
2026-XX-XX ... [INFO] Collected 150 rows -> data/raw/iris_raw.csv

Running stage 'preprocess':
> python src/pipeline/preprocess.py --input data/raw/iris_raw.csv --output data/processed/iris_preprocessed.csv
2026-XX-XX ... [INFO] Dropped 0 duplicate rows
2026-XX-XX ... [INFO] Preprocessed 150 rows -> data/processed/iris_preprocessed.csv

Running stage 'features':
> python src/pipeline/features.py ...
2026-XX-XX ... [INFO] Engineered 9 features -> data/processed/iris_features.csv

Running stage 'validate':
> python src/pipeline/validate.py ...
2026-XX-XX ... [INFO] Validation PASSED: 150 rows, 9 columns, all checks satisfied

Use `dvc push` to send your updates to remote storage.
