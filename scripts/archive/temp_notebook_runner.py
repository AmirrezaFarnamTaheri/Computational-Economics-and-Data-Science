import dask.dataframe as dd
import dask.array as da
from dask.distributed import Client

# Set up a local Dask cluster
client = Client()

# Dask DataFrame example
ddf = dd.demo.make_timeseries(
    '2000-01-01', '2000-01-31',
    freq='1s', partition_freq='1M', dtypes={'x': float, 'y': float, 'id': int}
)
mean_x_by_id = ddf.groupby('id').x.mean()
result = mean_x_by_id.compute()
print("Dask DataFrame result:")
print(result.head())

# Dask Array example
x = da.random.random((2000, 2000), chunks=(1000, 1000))
y = x.mean(axis=0)
result_array = y.compute()
print("\\nDask Array result:")
print(result_array.shape)
print(result_array[:10])

# Close the client
client.close()
