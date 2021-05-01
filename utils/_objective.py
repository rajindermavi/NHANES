from xgboost import XGBClassifier
from hyperopt import STATUS_OK
from sklearn.model_selection import cross_val_score

class Objective:
    def __init__(self, X, y, n_folds=10, scoring='f1_macro'):
        self.X = X
        self.y = y
        self.n_folds = n_folds
        self.scoring = scoring

    def func(self,params):
        """Objective function for Gradient Boosting Machine Hyperparameter Tuning"""
    
        clf = XGBClassifier(use_label_encoder=False,eval_metric = 'logloss')
        f1 = cross_val_score(clf, self.X, self.y, cv=self.n_folds, scoring=self.scoring)
        loss = 1 - max(f1)
        return {'loss': loss, 'params': params,'status':STATUS_OK}  