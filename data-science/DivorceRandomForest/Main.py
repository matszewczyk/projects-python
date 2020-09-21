from Functions import *

df = pd.read_csv('divorce.csv', delimiter=';')

accuracies = []
for i in range(100):
    train_df, test_df = train_test_split(df, 0.2)
    forest = random_forest(train_df, forest_size=7, sample_size=130, no_of_attributes=15)
    predictions = predict_forest(test_df, forest)
    accuracy = calculate_accuracy(predictions, test_df.Class)
    accuracies.append(accuracy)

mean_accuracy = sum(accuracies) / len(accuracies)
print(mean_accuracy)