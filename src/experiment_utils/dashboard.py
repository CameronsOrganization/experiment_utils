import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from bokeh.plotting import figure, show
from bokeh.io import output_notebook, curdoc
from bokeh.models import HoverTool
from bokeh.palettes import Category10

output_notebook(hide_banner=True)
curdoc().theme = "carbon"
colors = Category10[10]


from .utils import create_dataframe_from_nested_dict

pd.set_option("display.float_format", lambda x: "%.3e" % x)


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

    def plot_value(self, key, log_scale=False):
        df = (
            self.df_value(key)
            .reset_index()
            .melt("step", value_name="value", var_name="var")
        )
        p = figure(
            x_axis_label="Step",
            y_axis_label=key,
            y_axis_type="log" if log_scale else "linear",
        )
        for i, (legend_label, d) in enumerate(df.groupby("var")):
            d["color"] = colors[i % 10]
            p.line(
                "step",
                "value",
                source=d,
                legend_label=legend_label,
                line_width=2,
                color=colors[i % 10],
            )
            p.scatter(
                "step",
                "value",
                source=d.iloc[-1:],
                size=8,
                color=colors[i % 10],
                legend_label=legend_label,
                alpha=0.5,
            )
        p.add_tools(
            HoverTool(
                tooltips=[
                    ("Experiment", "@var"),
                    ("Step", "$x{0}"),
                    (key, "$y"),
                    ("Color", "$swatch:color"),
                ],
                mode="mouse",
                line_policy="none",
                muted_policy="ignore",
            )
        )
        p.sizing_mode = "stretch_width"
        p.legend.click_policy = "mute"
        p.legend.title = "Experiment"
        p.legend.title_text_font_style = "bold"
        p.legend.title_text_color = "white"
        p.legend.label_text_color = "white"
        p.legend.label_text_font_style = "bold"
        p.legend.background_fill_color = "black"
        p.legend.background_fill_alpha = 0.2
        p.yaxis.axis_label_text_font_size = "20pt"
        p.yaxis.major_label_text_font_size = "16pt"
        p.xaxis.major_label_text_font_size = "16pt"
        show(p)

    def __repr__(self):
        return f"Dashboard(log_path={self.log_path})"
