import numpy as np

from xgboost import XGBClassifier
from hyperopt import STATUS_OK
from sklearn.model_selection import cross_val_score

class Objective:
    def __init__(self,X_train,y_train,X_valid=None,y_valid=None,n_folds=5,scoring='f1_macro'):
        self.X_train = X_train
        self.y_train = y_train  
        self.X_valid = X_train if X_valid is None else X_valid
        self.y_valid = y_train if y_valid is None else y_valid 
        self.n_folds = n_folds
        self.scoring = scoring

    def func(self,params):
        """Objective function for Gradient Boosting Machine Hyperparameter Tuning"""
 
        clf = XGBClassifier(**params,use_label_encoder=False,eval_metric = 'logloss')
 
        f1 = cross_val_score(clf,self.X_train,self.y_train, cv=self.n_folds, scoring=self.scoring)
        loss = 1 - np.mean(f1)
        return {'loss': loss, 'params': params,'status':STATUS_OK}  