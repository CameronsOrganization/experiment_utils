import experiment_utils

import shutil

shutil.rmtree("./.logs")

logger = experiment_utils.Logger()
logger.start_experiment("test")

logger.log_param("param1", 1)
logger.log_params({"param3": 3, "param4": 4})
logger.log_param("param2", 2)

logger.log_value("value1", 1)
logger.log_values({"value2": 2, "value3": 3})

for i in range(10):
    logger.log_value("value4", 2 * i, i)

for i in range(10):
    logger.log_values({"value5": 3 * i, "value6": 4 * i}, i)

logger.log_metric("metric1", 1, experiment_utils.compare_fns.max)
logger.log_metrics({"metric2": 2, "metric3": 3}, experiment_utils.compare_fns.max)

for i in range(10):
    logger.log_metric("metric4", 2 * i, experiment_utils.compare_fns.max, i)

for i in range(10):
    logger.log_metrics(
        {"metric5": 3 * i, "metric6": 4 * i}, experiment_utils.compare_fns.max, i
    )

logger.log_metric("metric11", 1, experiment_utils.compare_fns.min)
logger.log_metrics({"metric12": 2, "metric13": 3}, experiment_utils.compare_fns.min)

for i in range(10):
    logger.log_metric("metric14", 2 * i, experiment_utils.compare_fns.min, i)

for i in range(10):
    logger.log_metrics(
        {"metric15": 3 * i, "metric16": 4 * i}, experiment_utils.compare_fns.min, i
    )


logger.end_experiment()
