# 2022-本科毕业设计源码
复现ATL03测高点云提取地表高程的过程。根据ICESat-2 ATL08土地和植被高度产品生成算法的理论基础编写Python脚本，搭建完成地表高程反演批处理工作流。

# 记得放ATL03文件到此目录


# 算法理论基础参考：2019_ICESat-2 ATBD for ATL08_r002_v2.pdf


# 下方 CMD 命令为使用 ATL03 数据反演地表面的脚本顺序运行命令。
## 经测试，待安装好 anaconda 环境后即可顺利运行。

## anaconda 环境
### 语言：Python 3.7
### 库：sys, os, shutil, numpy, csv, pandas, scipy, h5py, open3d, math, matplotlib, pyproj,  osgeo, gdal, gdalconst

## ---------- CMD 开始 ------------
conda activate python37（anaconda 环境）

E:

cd E:./script0830

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
## ---------- CMD 结束 ------------

## 该 CMD 命令将所有脚本完全运行结束，时间约花费 30 分钟。
## 倘若换为其他 ATL03 数据，则脚本 3_hist_Gauss_fit.py 中的参数暂时需要手动改变。
## 使用数学方法自动加载脚本 3_hist_Gauss_fit.py 参数的新版本脚本后续将在 github 更新。

## 此源码压缩包内容为 version_1 版本，未使用类、继承、多态等程序设计中提高代码利用率的方法。将在 version_2 版本优化代码，预计代码量将减少 1/5，运行速度也将进一步提高。
