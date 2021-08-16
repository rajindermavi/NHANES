# NHANES data for predictive analysis

This project collects data from the NHANES [website](https://www.cdc.gov/nchs/nhanes/index.htm) to create a data set for data exploration and predictive modeling.

## Data Collection

Data is collected over several steps in the NHANES/nhanes folder.

* GetData.ipynb: Collect raw data sets from the NHANES site and join them into a single relational table.

* PreProcessData.ipynb: Recode data into format useful for analysis and prediction.

* WrangleData.ipynb: Examine missing data. Drop records with excessive missing data. Split training/validation/test sets. Impute data using training set.

## EDA

* EDA.ipynb: In the EDA notebook, the hypertension target variable is created. The dataset is now ready for predictive analysis.

## Predictive Analysis

* HypertensiveML.ipynb: Several predictive models are constructed to predict hypertension from feature data. Note that all feature data can readily be obtained from a patient from a simple questionaire.