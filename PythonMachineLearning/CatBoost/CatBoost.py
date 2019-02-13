import Performance as performance
import Dataset as dataset
from matplotlib import pyplot as plt
from catboost import CatBoostClassifier

# Importing dataset
poker = dataset.Poker([0.2, 0.1, 0.7], 0.4)

# Loading model
#print('Loading existing model...')
#load_model("catboost_model", format='catboost')

# Creating model
print('Initializing model...')
model = CatBoostClassifier(
    task_type = 'GPU',
    thread_count = 8,
    num_trees = 700,
    depth = 10,
    learning_rate = 0.23,
    loss_function = 'MultiClass',
    eval_metric = 'TotalF1',
    classes_count = 10)

# Training
print('Training...')
model.fit(X = poker.X_train, y = poker.y_train, sample_weight = poker.train_sample_weights, eval_set = [(poker.X_validate, poker.y_validate)], verbose = True)

# Saving model
#print('Saving model...')
#model.save_model("catboost_model", format="cbm")

# Predicting
print('Predicting...')
y_pred = model.predict(poker.X_test, prediction_type='Class')

# Analytics
metric_results = model.get_evals_result()['learn']['MultiClass']
print('Plotting evaluation metric results...')
performance.plot_evaluation_metric_results(metric_results, "CatBoost - Evaluation metric results")
performance.print_advanced_metrics(y_pred, poker.y_test, poker.class_descriptions)
performance.plot_confusion_matrix(y_pred, poker.y_test, poker.class_labels, title = 'CatBoost - Confusion matrix', normalize = True)
plt.show()