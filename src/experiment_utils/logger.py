from typing import Any, Optional, Callable
import os
import yaml
import csv

from .utils import generate_id, validate_experiment_name, update_yaml


class Logger:
    def __init__(
        self,
        log_path: str = "./.logs/",
    ):
        self.log_path = log_path

    def is_experiment(self, experiment_path: str) -> bool:
        assert os.path.isdir(
            experiment_path
        ), f"Invalid experiment path: {experiment_path}"
        return True

    def start_experiment(self, experiment_name: Optional[str] = None) -> None:
        assert validate_experiment_name(
            experiment_name
        ), f"Invalid experiment name: {experiment_name}"
        self.experiment_name = experiment_name

        experiment_id = generate_id()

        if not os.path.isdir(self.log_path):
            os.makedirs(self.log_path)
        experiment_path = os.path.join(self.log_path, experiment_id)
        assert not os.path.isdir(
            experiment_path
        ), f"Experiment already exists: {experiment_path}"
        os.makedirs(experiment_path)
        self.experiment_id = experiment_id
        self.experiment_path = experiment_path

        with open(os.path.join(experiment_path, "meta.yaml"), "w") as f:
            yaml.dump(
                {
                    "experiment_id": experiment_id,
                    "experiment_name": experiment_name,
                },
                f,
            )

    def resume_experiment(self, experiment_path: str) -> None:
        self.is_experiment(experiment_path)
        self.experiment_path = experiment_path

    def end_experiment(self):
        self.is_experiment(self.experiment_path)
        self.experiment_path = None
        self.experiment_name = None
        self.experiment_id = None

    def log_param(self, key: str, value: Any):
        self.is_experiment(self.experiment_path)
        update_yaml(os.path.join(self.experiment_path, "params.yaml"), {key: value})

    def log_params(self, params: dict):
        self.is_experiment(self.experiment_path)
        update_yaml(os.path.join(self.experiment_path, "params.yaml"), params)

    def log_value(self, key: str, value: Any, step: Optional[int] = None):
        self.is_experiment(self.experiment_path)
        if not os.path.isdir(os.path.join(self.experiment_path, "values")):
            os.makedirs(os.path.join(self.experiment_path, "values"))
        file = os.path.join(self.experiment_path, "values", f"{key}.csv")
        if not os.path.isfile(file):
            with open(file, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["step", "value"])
        with open(file, "a") as f:
            writer = csv.writer(f)
            writer.writerow([step, value])

    def log_values(self, values: dict, step: Optional[int] = None):
        self.is_experiment(self.experiment_path)
        for key, value in values.items():
            self.log_value(key, value, step)

    def log_metric(
        self, key: str, value: Any, compare_fn: Callable, step: Optional[int] = None
    ):
        self.is_experiment(self.experiment_path)
        if not os.path.isdir(os.path.join(self.experiment_path, "metrics")):
            os.makedirs(os.path.join(self.experiment_path, "metrics"))
        file = os.path.join(self.experiment_path, "metrics", f"{key}.csv")
        if not os.path.isfile(file):
            with open(file, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["step", "value"])
        with open(file, "a") as f:
            writer = csv.writer(f)
            writer.writerow([step, value])

        file = os.path.join(self.experiment_path, "metrics.yaml")
        if os.path.isfile(file):
            with open(file, "r") as f:
                metrics = yaml.safe_load(f)
        else:
            metrics = {}
        metrics[key] = compare_fn(
            value,
            metrics.get(key, None),
        )
        with open(os.path.join(self.experiment_path, "metrics.yaml"), "w") as f:
            yaml.dump(metrics, f)

    def log_metrics(
        self, metrics: dict, compare_fn: Callable, step: Optional[int] = None
    ):
        self.is_experiment(self.experiment_path)
        for key, value in metrics.items():
            self.log_metric(key, value, compare_fn, step)

    def __repr__(self):
        return f"Logger(log_path={self.log_path})"
