import os
import yaml
import pandas as pd

from .utils import create_dataframe_from_nested_dict


class Dashboard:
    def __init__(
        self,
        log_path: str = "./.logs/",
    ):
        assert os.path.isdir(log_path), f"Invalid log path: {log_path}"
        self.log_path = log_path
        self.update()

    def update(self):
        assert os.path.isdir(self.log_path), f"Invalid log path: {self.log_path}"
        self.experiments = {}
        for experiment_path in os.listdir(self.log_path):
            experiment_path = os.path.join(self.log_path, experiment_path)
            if not os.path.isdir(experiment_path):
                continue

            file = os.path.join(experiment_path, "meta.yaml")
            if not os.path.isfile(file):
                continue
            with open(file, "r") as f:
                self.experiments[experiment_path] = {"meta": yaml.safe_load(f)}

            for file_name in ["params", "metrics"]:
                file = os.path.join(experiment_path, f"{file_name}.yaml")
                if not os.path.isfile(file):
                    continue
                with open(file, "r") as f:
                    self.experiments[experiment_path][file_name] = yaml.safe_load(f)

    def df(self):
        df = create_dataframe_from_nested_dict(self.experiments)

        def is_string_dtype(col):
            return col.dtype == "object" or pd.api.types.is_string_dtype(col.dtype)

        styles = [
            dict(selector=f"th.col_heading.level{i}", props=[("text-align", "left")])
            for i in range(2)
        ]
        styles += [
            {
                "selector": f"td:nth-child({df.columns.get_loc(col) + 1})",
                "props": [("text-align", "left")],
            }
            for col in df.columns
            if is_string_dtype(df[col])
        ]
        df = df.style.set_table_styles(styles)
        return df

    def __repr__(self):
        return self.show().to_string()
