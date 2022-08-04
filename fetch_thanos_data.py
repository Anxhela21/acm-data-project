from prometheus_api_client import PrometheusConnect
import pandas as pd
import datetime
from  operator import itemgetter
import argparse
url = "https://telemeter-lts.datahub.redhat.com/"
token = "6ZG_gNvPu6GSo89QYU9ap9tF_b3nZgexWBr2ezC5Nw4"
metrics_map = {'cpu_usage':'cluster:cpu_usage_cores:sum','mem_usage':'cluster:memory_usage_bytes:sum','api_server_count':'cluster:apiserver_current_inflight_requests:sum:max_over_time:2m','latencty':'{__name__="instance:etcd_network_peer_round_trip_time_seconds:histogram_quantile",quantile="0.99"}',
               'managed_clusters': 'acm_managed_cluster_info'}
metrics_to_fetch = ['api_server_count']
end_time = datetime.datetime.now() - datetime.timedelta(days=60)
#print(end_time)
step = '15m'
pc = PrometheusConnect(url=url, headers={"Authorization": "Bearer {}".format(token)}, disable_ssl=True)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--token ', dest='token',)
args = parser.parse_args()


def fetch_data_from_thanos(metrics, step, days=35, endtime=end_time):
    for metric in metrics:
        print(f'Currently fetching the metric: {metric}')
        metric_values = []
        start_time = endtime - datetime.timedelta(days=days)
        end_date = start_time
        for _ in range(days):
            start_date = end_date
            end_date = end_date + datetime.timedelta(days=1)
            # print(start_date,end_date)
            sample_metrics = pc.custom_query_range(
                query=metrics_map[metric],
                start_time=start_date,
                end_time=end_date,
                step=step
            )
            for element in sample_metrics:
                cluster_id = element['metric'].get('_id', '')
                metric_array = element['values']
                for metric_element in metric_array:
                    metric_element.append(cluster_id)
                metric_values.extend(metric_array)
        date_string = '_'.join(str(start_time.date()).split('-'))
        file_name = metric+'_' + date_string + '_' + str(days) + '_' + str(step)+'.csv'
        sample_df = pd.DataFrame(metric_values, columns=['timestamp', metric,'cluster_id'])
        print(sample_df.head())
        sample_df.timestamp = pd.to_datetime(sample_df.timestamp, unit="s")
        sample_df.to_csv(file_name, index=False)


def managed_cluster_info(metric,step,days=35,endtime=end_time):
    metric_values = []
    start_time = endtime - datetime.timedelta(days=days)
    end_date = start_time
    columns = ['_id','hub_cluster_id', 'managed_cluster_id','vendor']
    val = 1
    for _ in range(days):
        start_date = end_date
        end_date = end_date + datetime.timedelta(days=1)
        # print(start_date,end_date)
        sample_metrics = pc.custom_query_range(
            query=metric,
            start_time=start_date,
            end_time=end_date,
            step=step
        )
        for element in sample_metrics:
            metric_array = itemgetter('_id', 'hub_cluster_id', 'managed_cluster_id','vendor')\
                (element['metric'])
            metric_values.append(metric_array)
    cluster_info_df = pd.DataFrame(metric_values,columns=columns)
    date_string = '_'.join(str(start_time.date()).split('-'))
    filename = 'managed_cluster_'+date_string+'_'+str(days)+'_'+str(step)+'.csv'
    print(cluster_info_df.head())
    cluster_info_df.to_csv(filename, index=False)

#fetch_data_from_thanos(metrics_to_fetch, step, 35, end_time)
managed_cluster_info('acm_managed_cluster_info',step,35,end_time)
