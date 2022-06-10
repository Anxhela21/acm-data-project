# Data

## How to retrieve data

Data can be stored locally as parquet files by pulling and running a container image wrapping the obslytics tool modified for accessing Prometheus with bearer token authorization. In this director in your clone of the repo, run:

```sh
docker pull braet/obslytics-wrapper
```

After this, you should have the image in your local container registry. Before running the image, make copies of both example-input-config.yaml and example-output-config.yaml named input-config.yaml and output-config.yaml. The command running in the image relies on these file names for input. Then update the input-config file with your personal access token and the appropriate prometheus url, and specify the filename you'd like to store the container's output to in output-config. Finally, edit the conf.env file to contain the parameters you would like to use for your query: look at the in-file comments for more info.

Now you can actually run the container:

```sh
docker run -v $(pwd):/usr/src/io braet/obslytics-wrapper
```

After running, the parquet file will be saved in your PWD (this directory)

