
[![Documentation Status](https://readthedocs.org/projects/pywedge/badge/?version=main)](https://pywedge.readthedocs.io/en/main/?badge=main)  [![Downloads](https://pepy.tech/badge/pywedge)](https://pepy.tech/project/pywedge) [![PyPI version](https://badge.fury.io/py/pywedge.svg)](https://badge.fury.io/py/pywedge) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

# Pywedge

Pywedge is a [pip installable](https://pypi.org/project/pywedge/) Python package that intends to,

1. Quickly preprocess the data by taking the user’s preferred choice of pre-processing techniques & it returns the cleaned datasets to the user in the first step.

2. In the second step, Pywedge offers a baseline class that has a classification summary method & regression summary method, which can return ten various baseline models,        which can point the user to explore the best performing baseline model.

Pywedge intends to help the user by quickly preprocessing the data and to rightly point out the best performing baseline model for the given dataset so that the user can spend quality time tuning such a model algorithm.

# Pywedge Features
Cleans the raw data frame to fed into ML models. Following data pre_processing will be carried out,
1) segregating numeric & categorical columns
2) missing values imputation for numeric & categorical columns
3) standardization
4) feature importance
5) class oversampling using SMOTE
6) computes 10 different baseline models

# Pre_process_data()
Inputs: 
1) train = train dataframe
2) test = test dataframe
3) c = any redundant column to be removed (like ID column etc., at present supports a single column removal, subsequent version will provision multiple column removal requirements)
4) y = target column name as a string 
5) type = Classification(Default) / Regression

Returns:
1) new_X (cleaned feature columns in dataframe)
2) new_y (cleaned target column in dataframe)  
3) new_test (cleaned stand out test dataset)
```python
!pip install pywedge
import pywedge as pw
ppd = pw.Pre_process_data(train, test, c, y, type='Classification")
new_X, new_y, new_test = ppd.dataframe_clean()
```
![categorical_conversion](https://raw.githubusercontent.com/taknev83/pywedge/main/images/catcodes_2.JPG)

from the image, it can be observed that calling dataframe_clean method does the following,
1. Providing a summary of zero & missing values in the training dataset
2. Class balance summary
3. Categorical column conversion 

![standardization](https://raw.githubusercontent.com/taknev83/pywedge/main/images/Standardization.JPG)

user is asked for standardization choice...

![smote](https://raw.githubusercontent.com/taknev83/pywedge/main/images/smote.JPG)

For binary classification tasks, pywedge computes class balance & asks the user if oversampling using SMOTE to be applied to the data. 


# baseline_model()
- For classification - classification_summary() 
- For Regression - Regression_summary()

Inputs:
1) new_x
2) new_y

Returns:

Various baseline model metrics

Instantiate the baseline class & call the classification_summary method from baseline_model class,

```python
blm = pw.baseline_model(X,y)
blm.classification_summary()
```
![classification_summary](https://raw.githubusercontent.com/taknev83/pywedge/main/images/classification_summary.JPG)

The classification summary provides Top 10 feature importance (calculated using Adaboost feature importance) and asks for the test size from the user.

![cls_smry_2](https://raw.githubusercontent.com/taknev83/pywedge/main/images/classification_summary_2.JPG)

The classification summary provides baseline models of 10 different algorithms, user can identify best performing baseline models from the classification summary.

In the same way, regression analysis can be done using a few lines of code. 


### The following additions to pywedge is planned,
- [ ] To handle NLP column
- [ ] To handle time series dataset
- [ ] To handle stock prices specific analysis
- [ ] A separate method to produce good charts





Requires Python 64 bit

THIS IS IN BETA VERSION 
