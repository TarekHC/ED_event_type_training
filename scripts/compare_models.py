import argparse
from math import ceil
from pathlib import Path

import numpy as np

from event_types import event_types

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "An example script how to load trained models."
            "Remember not to use the data used to train these models."
            "In future perhaps also the test data will be saved."
        )
    )

    args = parser.parse_args()

    labels, train_features = event_types.nominal_labels_train_features()

    plot_predict_dist = True
    plot_scores = True
    plot_confusion_matrix = True
    plot_1d_conf_matrix = True
    n_types = 3
    type_bins = list(np.linspace(0, 1, n_types + 1))
    # type_bins = [0, 0.2, 0.8, 1]

    Path("plots").mkdir(parents=True, exist_ok=True)

    models_to_compare = [
        # 'linear_regression',
        # "random_forest",
        # "MLP_tanh",
        # 'MLP_relu',
        # 'MLP_logistic',
        # 'MLP_uniform',
        # 'MLP_lbfgs',
        # 'BDT',
        # 'BDT_small',
        # 'ridge',
        # 'SVR',
        # 'linear_SVR',
        # 'SGD',
    ]
    # models_to_compare = [
    #     'train_size_75p',
    #     'train_size_50p',
    #     'train_size_25p',
    #     'train_size_15p',
    #     'train_size_5p'
    # ]
    # models_to_compare = [
    #     "all_features",
    #     "no_reco_diff",
    # ]
    models_to_compare = [
        # "random_forest_300_15",
        # "random_forest_300_20",
        # "random_forest_500_15",
        # "random_forest_500_20",
        # "random_forest_2000_5",
        "MLP_tanh",
        # 'MLP_relu',
        # 'MLP_logistic',
        # 'MLP_uniform',
        # 'MLP_lbfgs',  # Do not use, very slow to train
        # 'MLP_tanh_large',
    ]

    if len(models_to_compare) > 1:
        group_models_to_compare = np.array_split(
            models_to_compare, ceil(len(models_to_compare) / 5)
        )
    else:
        group_models_to_compare = [models_to_compare]

    for i_group, these_models_to_compare in enumerate(group_models_to_compare):

        trained_models = event_types.load_models(these_models_to_compare)
        dataset_names = event_types.extract_unique_dataset_names(trained_models)
        dtf_e_test = event_types.load_multi_test_dtfs(dataset_names)

        if plot_predict_dist:
            for this_trained_model_name, this_trained_model in trained_models.items():
                plt = event_types.plot_test_vs_predict(
                    dtf_e_test, this_trained_model, this_trained_model_name
                )

                plt.savefig("plots/{}_predict_dist.pdf".format(this_trained_model_name))
                plt.savefig("plots/{}_predict_dist.png".format(this_trained_model_name))

            plt.clf()

        if plot_scores:
            plt, scores = event_types.plot_score_comparison(dtf_e_test, trained_models)
            plt.savefig("plots/scores_features_{}.pdf".format(i_group + 1))
            plt.savefig("plots/scores_features_{}.png".format(i_group + 1))
            plt.clf()
            event_types.save_scores(scores)

        if plot_confusion_matrix:

            dtf_test = event_types.add_predict_column(dtf_e_test, trained_models)

            event_type_log_e_bins = event_types.sensitivity_log_e_bins

            event_types_lists = event_types.partition_event_types(
                dtf_test, labels, event_type_log_e_bins, n_types=n_types, type_bins=type_bins, save_true_types=True
            )
            for this_trained_model_name, this_event_types in event_types_lists.items():
                plt = event_types.plot_confusion_matrix(
                    this_event_types, this_trained_model_name, n_types
                )

                plt.savefig(
                    "plots/{}_confusion_matrix_n_types_{}.pdf".format(
                        this_trained_model_name, n_types
                    )
                )
                plt.savefig(
                    "plots/{}_confusion_matrix_n_types_{}.png".format(
                        this_trained_model_name, n_types
                    )
                )

                if plot_1d_conf_matrix:

                    plt = event_types.plot_1d_confusion_matrix(
                        this_event_types, this_trained_model_name, n_types
                    )

                    plt.savefig(
                        "plots/{}_1d_confusion_matrix_n_types_{}.pdf".format(
                            this_trained_model_name, n_types
                        )
                    )
                    plt.savefig(
                        "plots/{}_1d_confusion_matrix_n_types_{}.png".format(
                            this_trained_model_name, n_types
                        )
                    )

                plt.clf()
