import pandas as pd
import numpy as np
import random


def train_test_split(df, test_size):
    test_size = round(test_size * len(df))

    indexes = df.index.tolist()
    test_indexes = random.sample(population=indexes, k=test_size)

    test_df = df.loc[test_indexes]
    train_df = df.drop(test_indexes)

    return train_df, test_df


def sample_data(train_df, sample_size):
    sample_indexes = np.random.randint(low=0, high=len(train_df), size=sample_size)
    sampled_data = train_df.iloc[sample_indexes]

    return sampled_data


def unique_check(data):
    label_column = data[:, -1]
    unique_classes = np.unique(label_column)

    if len(unique_classes) == 1:
        return True
    else:
        return False


def classify(data):
    label_column = data[:, -1]
    unique_classes, counts_unique_classes = np.unique(label_column, return_counts=True)

    index = counts_unique_classes.argmax()
    classification = unique_classes[index]

    return classification


def entropy_calc(data):
    label_column = data[:, -1]
    values, counts = np.unique(label_column, return_counts=True)

    probabilities = counts / counts.sum()
    entropy = -sum(probabilities * np.log(probabilities))
    return entropy


def global_entropy_calc(data_true, data_false):
    n = len(data_true) + len(data_false)
    p_data_true = len(data_true) / n
    p_data_false = len(data_false) / n
    global_entropy = (p_data_true * entropy_calc(data_true)
                      + p_data_false * entropy_calc(data_false))
    return global_entropy


def find_split(data, no_of_attributes):
    column_indexes = list(range(54))
    column_indexes = random.sample(population=column_indexes, k=no_of_attributes)

    values = [0, 1, 2, 3, 4]
    global_entropy = 10
    for column_index in column_indexes:
        for value in values:

            split_column_values = data[:, column_index]
            data_true = data[split_column_values == value]
            data_false = data[split_column_values != value]
            current_global_entropy = global_entropy_calc(data_true, data_false)

            if current_global_entropy <= global_entropy:
                global_entropy = current_global_entropy
                best_split_column = column_index
                best_split_value = value

    split_column_values = data[:, best_split_column]
    data_true = data[split_column_values == best_split_value]
    data_false = data[split_column_values != best_split_value]

    return best_split_column, best_split_value, data_true, data_false


def decision_tree(df, no_of_attributes, counter=0):

    if counter == 0:
        global DATA_LABELS
        DATA_LABELS = df.columns
        data = df.values
    else:
        data = df
    if (unique_check(data)):
        classification = classify(data)
        return classification

    if len(data) == 0:
        return

    else:
        counter += 1
        split_column, split_value, data_true, data_false = find_split(data, no_of_attributes)

        data_label = DATA_LABELS[split_column]
        question = "{} = {}".format(data_label, split_value)

        sub_tree = {question: []}

        yes_answer = decision_tree(data_true, counter, no_of_attributes)
        no_answer = decision_tree(data_false, counter, no_of_attributes)

        sub_tree[question].append(yes_answer)
        sub_tree[question].append(no_answer)

        return sub_tree


def predict(observation, tree):
    question = list(tree.keys())[0]
    feature_name, comparison_operator, value = question.split(" ")

    if str(observation[feature_name]) == value:
        answer = tree[question][0]
    else:
        answer = tree[question][1]

    if not isinstance(answer, dict):
        return answer

    else:
        remaining_tree = answer
        return predict(observation, remaining_tree)


def predict_all(test_df, tree):
    predictions = test_df.apply(predict, args=(tree,), axis=1)
    return predictions


def random_forest(train_df, forest_size, sample_size, no_of_attributes):
    forest = []
    for i in range(forest_size):
        sampled_data = sample_data(train_df, sample_size)
        tree = decision_tree(sampled_data, no_of_attributes=no_of_attributes)
        forest.append(tree)

    return forest


def predict_forest(test_df, forest):
    df_predictions = {}
    for i in range(len(forest)):
        column_name = "tree_{}".format(i)
        predictions = predict_all(test_df, tree=forest[i])
        df_predictions[column_name] = predictions

    df_predictions = pd.DataFrame(df_predictions)
    random_forest_predictions = df_predictions.mode(axis=1)[0]
    return random_forest_predictions


def calculate_accuracy(predictions, labels):
    predictions_correct = predictions == labels
    accuracy = predictions_correct.mean()

    return accuracy
