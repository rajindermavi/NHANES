
import pandas as pd  
from sklearn.utils.validation import check_is_fitted
from sklearn.base import BaseEstimator, TransformerMixin


class GroupImputer(BaseEstimator, TransformerMixin):
    '''
    Class used for imputing missing values in a pd.DataFrame using either mean or median of a group.
    
    Parameters
    ----------    
    group_cols : list
        List of columns used for calculating the aggregated value 
    target : str
        The name of the column to impute
    metric : str
        The metric to be used for remplacement, can be one of ['mean', 'median']
    Returns
    -------
    X : array-like
        The array with imputed values in the target column
    -------
    Based on code from
    https://gist.github.com/erykml/5e8881bd1e27eb6aa04161880228dbaf#file-custom_imputer_4-py
    '''
    def __init__(self, group_cols, target, metric='mean'):
        
        assert metric in ['mean', 'median','mode'],\
            'Unrecognized value for metric, should be mean, median, or mode'
        assert type(group_cols) == list,\
            'group_cols should be a list of columns'
        assert type(target) == str, 'target should be a string'
        
        self.group_cols = group_cols
        self.target = target
        if metric in ['mean','median']:
            self.metric = metric
        else:
            self.metric = pd.Series.mode
    
    def fit(self, X, y=None):
        
        assert pd.isnull(X[self.group_cols]).any(axis=None) == False,\
            'There are missing values in group_cols'
        
        impute_map = X.groupby(self.group_cols)[self.target]\
            .agg(self.metric).reset_index(drop=False)
        
        self.impute_map_ = impute_map
        
        return self 
    
    def transform(self, X, y=None):
        
        # make sure that the imputer was fitted
        check_is_fitted(self, 'impute_map_')
        
        X = X.copy()
        
        for index, row in self.impute_map_.iterrows():
            ind = (X[self.group_cols] == row[self.group_cols]).all(axis=1)
            X.loc[ind, self.target] = X.loc[ind, self.target].fillna(row[self.target])
        
        return X.values
    
    
    
class ContinuousImputer(BaseEstimator, TransformerMixin):
    '''
    Class used for imputing missing values in a pd.DataFrame using window averaged value column
    
    Parameters
    ----------    
    col : str
        column used for calculating the window aggregated value 
    target : str
        The name of the column to impute
    window : int
        Width of window for averaging
    Returns
    -------
    X : array-like
        The array with imputed values in the target column
    -------
    Based on code from
    https://gist.github.com/erykml/5e8881bd1e27eb6aa04161880228dbaf#file-custom_imputer_4-py
    '''
    def __init__(self, group_col, target, window):
        
        assert type(window) == int and window > 0,\
            'Window value should be a positive integer'
        assert type(group_col) == str, 'col should be a string'
        assert type(target) == str, 'target should be a string'
        
        self.group_col = group_col
        self.target = target
        self.window = window
    
    def fit(self, X, y=None):
        
        assert pd.isnull(X[self.group_col]).any(axis=None) == False,\
            'There are missing values in group_col'
        
        impute_map = X[[self.group_col,self.target]]\
            .groupby(by = [self.group_col])\
            .median().rolling(window = self.window, center = True)\
            .mean().interpolate(limit_direction = 'both')
        
        self.impute_map_ = impute_map
        
        return self 
    
    def transform(self, X, y=None):
        
        # make sure that the imputer was fitted
        check_is_fitted(self, 'impute_map_')
        
        X = X.copy()
        
        for index, row in self.impute_map_.iterrows():
            ind = (X[self.group_col] == row.name)
            X.loc[ind, self.target] = X.loc[ind, self.target]\
                .fillna(row[self.target]).round()
        
        return X.values    