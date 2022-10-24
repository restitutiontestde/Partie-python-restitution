# coding=utf-8
from etl_src.workers.Extract import ExtratJob
from etl_src.workers.Transfom import TransformJob
from etl_src.workers.Load import LoadJob


# Extract job 
ExtratJob().run_worker()

# Transform job
TransformJob().run_worker()

# Load job 
LoadJob().run_worker()




