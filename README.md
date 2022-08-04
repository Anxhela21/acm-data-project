# acm-data-project

## What's this?

The acm-data-project is a python notebook workspace for extracting and profiling cluster metrics collected as a part of the Advanced Cluster Management observability functions. These notebooks interface with Prometheus to query this time-series data and serve as a place for exploration of patterns in cluster metrics.

## Dependencies
```sh
python3 -m pip install matplotlib
python3 -m pip install pyarrow
python3 -m pip install pandas
python3 -m pip install prometheus-api-client
```

## Data Analytics

The above notebooks are trying to understand different metrics that are pulled from prometheus, finding any patterns in the cluster metric usage and also label abnormal cluster usage as an anomaly.

time_series_analysis.ipynb -- This notebook is experimenting all the statistiscal arima models inorder to understand timeseries forecasting 

fetch_thanos_data.py -- This script is responsible to fetch the metrics from thanos/prometheus. It takes the number of days, the list of metrics and API Token as an input and create seperate csv files for each of the metric 

managed_cluster_preprocessing.ipynb -- This notebook is trying to preprocess the csv files gathered using above method and trying to get the information whether the cluster is either managed or hub cluster

metric_preprocessing.ipynb -- This notebook is trying to create new indexes and trying to handle all the NaN values and create static features from the time series metrics and saving them in the csv file

dimentionality_reduction_anomaly.ipynb -- This notebook is responsible to perform, standardization, normalization, dimentionality reduction, clustering / anomaly detection.


