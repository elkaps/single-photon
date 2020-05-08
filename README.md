# single-photon

## Requirements

For converting the Hydra Harp ht2 files to csv [libpicoquant](https://github.com/tsbischof/libpicoquant) is used.

For Installation refer to https://github.com/tsbischof/libpicoquant/blob/master/INSTALL

## Data preparation

To convert the ht2 files to csv you can use:

```python
python3 utils/ht2_to_csv.py --format ht2 <PATH_TO_FOLDER>
```

or for MATLAB mat files:

```python
python3 utils/ht2_to_csv.py --format mat <PATH_TO_FOLDER>
```

Alternative: The data can also be saved as a csv using MATLAB