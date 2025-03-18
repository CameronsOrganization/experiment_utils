import experiment_utils

import shutil
import os

if os.path.isdir("./.logs"):
    shutil.rmtree("./.logs")

logger = experiment_utils.Logger()
logger.start_experiment("test")

logger.log_param("param1", 1)
logger.log_params({"param3": 3, "param4": 4})
logger.log_param("param2", 2)

logger.log_value("value1", 1)
logger.log_values({"value2": 2, "value3": 3})

for i in range(10):
    logger.log_value("value4", 2 * i, step=i)

for i in range(10):
    logger.log_values({"value5": 3 * i, "value6": 4 * i}, step=i)

logger.log_value("metric1", 1, compare_fn=experiment_utils.compare_fns.max)
logger.log_values(
    {"metric2": 2, "metric3": 3}, compare_fn=experiment_utils.compare_fns.max
)

for i in range(10):
    logger.log_value(
        "metric4", 2 * i, step=i, compare_fn=experiment_utils.compare_fns.max
    )

for i in range(10):
    logger.log_values(
        {"metric5": 3 * i, "metric6": 4 * i},
        step=i,
        compare_fn=experiment_utils.compare_fns.max,
    )


logger.log_value("metric11", 1, compare_fn=experiment_utils.compare_fns.min)
logger.log_values(
    {"metric12": 2, "metric13": 3}, compare_fn=experiment_utils.compare_fns.min
)

for i in range(10):
    logger.log_value(
        "metric14", 2 * i, step=i, compare_fn=experiment_utils.compare_fns.min
    )

for i in range(10):
    logger.log_values(
        {"metric15": 3 * i, "metric16": 4 * i},
        step=i,
        compare_fn=experiment_utils.compare_fns.min,
    )

logger.end_experiment()
