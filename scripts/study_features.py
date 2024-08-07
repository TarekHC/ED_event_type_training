import argparse
import copy

from event_types import event_types

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Train regressor models with various training features."
            "Results are saved in the models directory."
        )
    )

    args = parser.parse_args()

    labels, train_features = event_types.nominal_labels_train_features()

    features = dict()
    features["all_features"] = train_features
    features["no_reco_diff"] = copy.copy(train_features)
    for feature_name in train_features:
        if feature_name.endswith("log_reco_diff"):
            features["no_reco_diff"].remove(feature_name)
    # features['no_length'] = copy.copy(train_features)
    # for feature_name in train_features:
    #     if feature_name.endswith('_length'):
    #         features['no_length'].remove(feature_name)
    # features['no_dispCombine'] = copy.copy(train_features)
    # for feature_name in train_features:
    #     if feature_name.endswith('_dispCombine'):
    #         features['no_dispCombine'].remove(feature_name)
    # features['old_features'] = copy.copy(train_features)
    # for feature_name in train_features:
    #     if any(feature_name.endswith(suffix) for suffix in ['_width', '_length', '_dispCombine']):
    #         features['old_features'].remove(feature_name)

    models_to_train = dict()
    all_models = event_types.define_regressors()
    for features_name, these_features in features.items():
        print(features_name, these_features)
        models_to_train[features_name] = dict()
        models_to_train[features_name]["train_features"] = these_features
        models_to_train[features_name]["labels"] = labels
        models_to_train[features_name]["model"] = all_models["MLP_tanh"]
        models_to_train[features_name]["test_data_suffix"] = "default"

    start_from_DL2 = False
    bins_off_axis_angle = [0, 1, 2, 3, 4, 5]
    layout_desc = "N.D25-4LSTs09MSTs-MSTN"  # LaPalma
    # layout_desc = 'S-M6C8aj-14MSTs37SSTs-MSTF'  # Paranal
    if start_from_DL2:
        dl2_file_names = [
            "../../data/LongFiles/North/"
            f"gamma_cone.{layout_desc}_ID0.eff-{i}.root" for i in bins_off_axis_angle
        ]
        dtf = event_types.extract_df_from_multiple_dl2(dl2_file_names)
    else:
        dtf = event_types.load_dtf(
            [f"gamma_cone.{layout_desc}_ID0.eff-{i}" for i in bins_off_axis_angle]
        )

    dtf = dtf.dropna()

    dtf_e = event_types.bin_data_in_energy(dtf, n_bins=20)

    dtf_e_train, dtf_e_test = event_types.split_data_train_test(
        dtf_e, test_size=0.75, random_state=777
    )

    trained_models = event_types.train_models(dtf_e_train, models_to_train)
    event_types.save_models(trained_models)
    event_types.save_test_dtf(dtf_e_test)
