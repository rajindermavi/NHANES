# NHANES data for predictive analysis

This project collects data from the NHANES [website](https://www.cdc.gov/nchs/nhanes/index.htm) to create a data set for data exploration and predictive modeling.

## Data Collection

Data is collected over several steps in the NHANES/nhanes folder.

* GetData: Collect raw data sets from the NHANES site and join them into a single relational table.

* PreProcessData: Recode data into format useful for analysis and prediction.

* WrangleData: Examine missing data. Drop records with excessive missing data. Split training/validation/test sets. Impute data using training set.

## EDA

In the EDA notebook, the hypertension target variable is created. The dataset is now ready for predictive analysis.