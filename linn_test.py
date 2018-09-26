# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import sklearn
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV


# Splitte data
def split(df, test_size=0.25, rstate=42):
    """Split in to X and y, and
    train and test"""
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size, random_state=rstate)
    return (X_train, X_test, y_train, y_test)


def RF_reg(X_train, X_test, y_train, y_test):
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
    return trainscore, testscore, list(pred)


if __name__ == '__main__':
    data_532 = pd.read_csv('C:/Users/LES/PycharmProjects/Ny_filtype/532-vegref.csv',
                       sep=';', index_col='vegreferanse')
    data_532['var1'] = np.random.randint(2, size=len(data_532.index))
    data_532['var2'] = np.random.randint(2, size=len(data_532.index))
    data_532 = data_532.iloc[:,-2:]
    data_532['ulykke'] = np.random.randint(30, size=len(data_532.index)).astype('float64')
    X_train, X_test, y_train, y_test = split(data_532)
    trainscore, testscore, pred = RF_reg(X_train, X_test, y_train, y_test)