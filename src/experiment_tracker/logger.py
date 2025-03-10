from typing import Any, Optional, Callable
import os

from .utils import generate_id, validate_experiment_name


class Logger:
    def __init__(
        self,
        log_dir: str = "./logs/",
    ):
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        self.log_dir = log_dir

    def start_experiment(self, experiment_name: Optional[str] = None):
        assert validate_experiment_name(
            experiment_name
        ), f"Invalid experiment name: {experiment_name}"
        experiment_id = generate_id()
        assert os.path.isdir(self.log_dir), f"Invalid log directory: {self.log_dir}"
        experiment_dir = os.path.join(self.log_dir, experiment_id)
        assert not os.path.isdir(
            experiment_dir
        ), f"Experiment already exists: {experiment_dir}"
        os.makedirs(experiment_dir)
        self.experiment_id = experiment_id

    def resume_experiment(self, experiment_id: str):
        assert os.path.isdir(
            os.path.join(self.log_dir, experiment_id)
        ), f"Invalid experiment id: {experiment_id}"
        self.experiment_id = experiment_id

    def end_experiment(self):
        self.experiment_id = None

    def log_param(self, key: str, value: Any):
        pass

    def log_params(self, params: dict):
        pass

    def log_value(self, key: str, value: Any, step: Optional[int] = None):
        pass

    def log_values(self, values: dict, step: Optional[int] = None):
        pass

    def log_metric(
        self, key: str, value: Any, compare_fn: Callable, step: Optional[int] = None
    ):
        pass

    def __repr__(self):
        pass
