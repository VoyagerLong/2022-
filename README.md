# 2022 - Undergraduate Thesis Source Code

This repository contains a complete workflow for extracting ground elevation from ATL03 photon data, based on the ATL08 land and vegetation height product algorithms from ICESat-2. The project reproduces the theoretical basis and implements it using Python scripts for batch processing of surface elevation inversion.

## 📚 Algorithm Reference

- Theoretical basis: `2019_ICESat-2 ATBD for ATL08_r002_v2.pdf`

## 🚀 Execution Instructions (Windows CMD)

Below are the sequential commands to run scripts for surface inversion using ATL03 data. Tested and verified in the Anaconda environment.

> Note: All scripts assume you are in the `E:/script0830` directory.

### ✅ Environment Setup

- Language: Python 3.7
- Required packages:
  ```
  sys, os, shutil, numpy, csv, pandas, scipy, h5py, open3d,
  math, matplotlib, pyproj, osgeo, gdal, gdalconst
  ```

### ▶️ CMD Commands

```cmd
conda activate python37

E:

cd E:/script0830

python 1_extract_and_norm_t_h_3rdd=0.py

cd ./output

python 2_open3d_k_20_histogram_x为t.py

cd ./1

python 3_hist_Gauss_fit.py
python 4_get_signal.py
python 5_4326_proj_4550.py
python 6_variable_windows.py
python 7_De_trend_Median_filt.py
python 8_De_trend_ref_DEM_limit.py
python 9_De_trend_Asmooth插值.py
python 10_De_trend_5to95_heights.py
python 11_De_trend_median+average_filt_10times.py
python 12_filter_outlier_noise_150m.py
python 13_filter_outlier_noise_Detrend.py
python 14_filter_outlier_noise_2std.py
python 15_filter_outlier_noise_Asmooth插值.py
python 16_filter_outlier_noise_Median_filt.py
python 17_filter_outlier_noise_median+average_filt_10times.py
python 18_filter_outlier_noise_Detrend.py
python 19_initial_ground_estimate_cutOff_lowerbound.py
python 0_view_19.py
python 20_initial_ground_estimate_potential_ground_points.py
python 0_view_20.py
python 21_initial_ground_estimate_cutOff_upperbound.py
python 0_view_21.py
python 22_initial_ground_estimate_ground_points.py
python 0_view_22.py
python 23_initial_ground_estimate_refine_ground.py
python 0_view_23.py
python 24_initial_ground_estimate_final_ground_points.py
python 0_view_24.py

exit
```

> ⏱️ Estimated runtime for all scripts: ~30 minutes.

## ⚠️ Notes

- When using different ATL03 datasets, manual adjustment may be needed for parameters in `3_hist_Gauss_fit.py`.
- A future update will automate this parameter tuning.
- This is version 1 of the code and does not yet use object-oriented features such as classes or inheritance.
- Version 2 will include optimized code structure, reducing code size by ~20% and improving execution speed.

## 📷 Visual Examples

![Gauss_fit](https://github.com/juejue123/2022-/assets/82886491/aa275da1-6b80-4601-ad6c-6584158d637d)
![Final Ground Points](https://github.com/juejue123/2022-/assets/82886491/b6d4b2ef-9f20-472d-bc8d-e2b867226310)
