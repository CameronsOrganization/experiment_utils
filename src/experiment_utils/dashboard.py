import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from .utils import create_dataframe_from_nested_dict


class Dashboard:
    def __init__(
        self,
        log_path: str = "./.logs/",
    ):
        assert os.path.isdir(log_path), f"Invalid log path: {log_path}"
        self.log_path = log_path

    def df(self):
        assert os.path.isdir(self.log_path), f"Invalid log path: {self.log_path}"
        experiments = {}
        for experiment_path in os.listdir(self.log_path):
            experiment_path = os.path.join(self.log_path, experiment_path)
            if not os.path.isdir(experiment_path):
                continue

            file = os.path.join(experiment_path, "meta.yaml")
            if not os.path.isfile(file):
                continue
            with open(file, "r") as f:
                experiments[experiment_path] = {"meta": yaml.safe_load(f)}

            for file_name in ["params", "values"]:
                file = os.path.join(experiment_path, f"{file_name}.yaml")
                if not os.path.isfile(file):
                    continue
                with open(file, "r") as f:
                    experiments[experiment_path][file_name] = yaml.safe_load(f)

        experiments = create_dataframe_from_nested_dict(experiments)

        def is_string_dtype(col):
            return col.dtype == "object" or pd.api.types.is_string_dtype(col.dtype)

        styles = [
            dict(selector=f"th.col_heading.level{i}", props=[("text-align", "left")])
            for i in range(2)
        ]
        styles += [
            {
                "selector": f"td:nth-child({experiments.columns.get_loc(col) + 1})",
                "props": [("text-align", "left")],
            }
            for col in experiments.columns
            if is_string_dtype(experiments[col])
        ]
        experiments = experiments.style.set_table_styles(styles)
        return experiments.data

    def df_value(self, key):
        assert os.path.isdir(self.log_path), f"Invalid log path: {self.log_path}"
        experiments = []
        for experiment_path in os.listdir(self.log_path):
            experiment_path = os.path.join(self.log_path, experiment_path)
            if not os.path.isdir(experiment_path):
                continue

            file = os.path.join(experiment_path, "meta.yaml")
            if not os.path.isfile(file):
                continue
            with open(file, "r") as f:
                experiment_id = yaml.safe_load(f)["experiment_id"]

            file = os.path.join(experiment_path, "values", f"{key}.csv")
            if not os.path.isfile(file):
                continue
            with open(file, "r") as f:
                df = pd.read_csv(f, index_col=0)
                df.rename(columns={df.columns[0]: experiment_id}, inplace=True)
                experiments += [df]
        experiments = pd.concat(experiments, axis=1)
        return experiments

    def plot_value(self, key):
        df = self.df_value(key)
        for col in df.columns:
            d = df[col]
            d = d[d.notna()][d.notnull()]
            plt.plot(d, label=col)
        # plt.plot(df)
        plt.xlabel("Step")
        plt.ylabel(key)
        plt.legend(df.columns)
        plt.show()

    def __repr__(self):
        return f"Dashboard(log_path={self.log_path})"
