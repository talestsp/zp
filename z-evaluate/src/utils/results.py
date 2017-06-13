from uuid import uuid4
from datetime import datetime
import pytz
import json

from src.plot.plot import prediction_scatter_plot
from src.utils.path_manager import PathManager

from pandas import set_option
set_option('display.float_format', lambda x: '%.5f' % x)


class Results:

    def __init__(self, model, result_df, mae, r2, tags=[]):
        self.id = uuid4()
        self.datetime = datetime.now(pytz.timezone("Brazil/East")).__str__().split(".")[0]
        self.model_name = model.get_model_name()
        self.result_df = result_df
        self.params = model.params()
        self.mae = mae
        self.r2 = r2
        self.tags = tags
        self.model = model
        self.new_features = None

    def save(self):
        results_file_path = PathManager().get_results_data_eval_dir() + self.id.__str__() + ".json"
        with open(results_file_path, 'w') as file:
            json.dump(self.result_dict(), file)

        plot_file_path = PathManager().get_results_plot_dir() + self.id.__str__() + ".html"
        self.plot(show=False, save=True, file_name=plot_file_path)

        result_df_file_path = PathManager().get_results_predictions_eval_dir() + self.id.__str__() + ".csv"
        self.result_df.to_csv(result_df_file_path, index=False)

    def show_plot(self):
        self.plot(show=True, save=False)

    def plot(self, show, save, file_name=None):
        title = self.model_name + " " + "mae:" + str(round(self.mae, 5)) + " " + "r2:" + str(round(self.r2, 5)) + " " + "tags:" + str(self.tags)
        prediction_scatter_plot(self.result_df, show_plot=show, save_plot=save, title=title, file_name=file_name)

    def columns_relevance(self):
        return self.model.columns_relevance()

    def print(self):
        print("id:", self.id)
        #print("model:" + self.model_name)
        print("Date:", self.datetime)
        print("MAE:", self.mae)
        print("R2:", self.r2)
        print("tags:", self.tags)
        print("columns relevance")
        #print(self.columns_relevance())
        print()

    def result_dict(self):
        result_dict = {}
        result_dict["id"] = self.id.__str__()
        result_dict["date"] = self.datetime
        result_dict["model_name"] = self.model_name
        result_dict["mae"] = self.mae
        result_dict["r2"] = self.r2
        result_dict["tags"] = self.tags
        result_dict["params"] = self.params
        result_dict["new_features"] = self.new_features

        return result_dict

    def result_json(self):
        result_dict = self.result_dict()
        return json.dumps(result_dict)

    def set_new_features(self, new_features):
        self.new_features = new_features
