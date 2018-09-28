# -*- coding: utf-8 -*-

"""
Modell
"""
import os
from config import basedir
import pandas as pd
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt


# Splitte data
def split(df, test_size=0.25, rstate=42):
    """
    Split in to X and y, and
    train and test
    """
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size,
                                                        random_state=rstate)
    return (X_train, X_test, y_train, y_test)


def RF_reg(X_train, X_test, y_train, y_test):
    """
    :param X_train: Features for training data
    :param X_test: Features for test data
    :param y_train: Respons for train data
    :param y_test: Respons for test data
    :return:trainscore, testscore, list of predictions, classifier
    """
    pipe_forest = make_pipeline(StandardScaler(), RandomForestRegressor())
    n_estimators = np.arange(5, 200, 10)
    max_features = ['auto', 'sqrt']
    max_depth = np.append(np.arange(10, 110, 10), None)
    min_samples_split = [2, 5, 10]
    min_samples_leaf = [1, 2, 4]
    bootstrap = [True, False]
    param_grid_forest = [{'randomforestregressor__n_estimators': [5],
                          'randomforestregressor__max_features': max_features,
                          'randomforestregressor__max_depth': max_depth,
                          'randomforestregressor__min_samples_split': [2],
                          'randomforestregressor__min_samples_leaf': [1],
                          'randomforestregressor__bootstrap': [True]}]

    grid = GridSearchCV(estimator=pipe_forest, param_grid=param_grid_forest,
                        cv=5, n_jobs=-1)
    gs = grid.fit(X_train, y_train)
    trainscore = gs.best_score_
    clf = gs.best_estimator_
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    testscore = clf.score(X_test, y_test)
    print(gs.best_params_)
    imp = clf.steps[1][1].feature_importances_
    return trainscore, testscore, list(pred), clf, imp

def lin_regplot(X, y, model):
    plt.scatter(X[:, 0], y, c='lightblue', label='observasjoner')
    plt.plot(X[:, 0], model.predict(X), color='red', linewidth=2,
             label='modell')
    plt.legend()
    #plt.legend()
    plt.xlabel('var1')
    plt.ylabel('ulykker')

    plt.show()
    return


def change_var(df, var, value, model):
    """

    """
    data = df.copy()
    data[var] += value
    # old = clf.predict(df)
    new = model.predict(data.iloc[:, :-1]).astype(int)
    data['predikerte ulykker'] = new
    diff = new - df['trafikk_ulykke']

    diff = ((new - df['trafikk_ulykke']) / df['trafikk_ulykke']) * 100
    data['ulykker før endring'] = df['trafikk_ulykke']
    data['forskjell %'] = round(diff, 1)
    data['forskjell'] = diff
    #data = data.sort_values('ulykker før endring', ascending=False)
    data = data.sort_values('forskjell', ascending=True)
    return data

def modell(kolonne, endring):
    datafile = os.path.join(basedir, 'datasett.csv')
    data_ = pd.read_csv(datafile, index_col=0)
    X_train, X_test, y_train, y_test = split(data_)
    trainscore, testscore, pred, clf, imp = RF_reg(X_train, X_test, y_train,
                                                   y_test)
    new_data = change_var(data_, kolonne, endring, model=clf)
    new_data.fartsdempere.astype(int)
    new_data.trafikk_mengde.astype(int)
    return new_data.iloc[:20,:].to_html(classes="ui striped table",
        border = 0,
        justify = 'left',
        columns = ['trafikk_mengde','fartsgrense','predikerte ulykker',
                   'ulykker før endring','forskjell %'])


def reality():
    datafile = os.path.join(basedir, 'datasett.csv')
    df = pd.read_csv(datafile,
                   index_col=0)
    df_sort = df.sort_values('trafikk_ulykke', ascending=False)
    df_sort = df_sort.astype(int)
    return df_sort.iloc[0:20, :].to_html(classes="ui striped table",
        border=0,
        justify = 'left')

if __name__ == '__main__':
    res = modell(kolonne='trafikk_mengde', endring= -10)
    print(np.shape(res))
    print(res)



