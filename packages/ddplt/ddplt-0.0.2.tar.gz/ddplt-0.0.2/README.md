# ddplt

[![PyPI version](https://badge.fury.io/py/ddplt.svg)](https://badge.fury.io/py/ddplt)

A package with code from my ML projects that has a potential of being reusable.

## Installation

The package installation is simple, since the repo is available on PyPi:
```bash
pip install ddplt
```

## Confusion matrix

Draw a confusion matrix for classification results:
```python
import numpy as np
from ddplt.heatmaps import draw_confusion_heatmap

# generate some data 
y_test = np.array([0, 0, 1, 1, 2, 0])
y_pred = np.array([0, 1, 1, 2, 2, 0])
class_names = np.array(['hip', 'hop', 'pop'])
ax, cm = draw_confusion_heatmap(y_test, y_pred, class_names)
```
![conf_matrix](img/cm_hip_hop_pop.png)

## Cross-validated *receiver operating characteristic* and *precision-recall* curves

Draw *receiver operating characteristic* (ROC) and *precision-recall* (PR) curves using *k*-fold cross-validation:
```python
from ddplt.classification import draw_roc_prc_cv

from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

X, y = make_moons(500, noise=.2, random_state=123)
estimator = LogisticRegression()
cv = KFold(n_splits=5, shuffle=True, random_state=123)

draw_roc_prc_cv(estimator, X, y, cv)
```
![roc_prc_cv](img/roc_prc_cv.png)


The function `draw_roc_prc_cv` accepts the following parameters:
- `estimator` - Scikit-learn's estimator with set hyperparameters. The estimator does not have to be fitted.
- `X` - array-like with shape `(n_instances,n_features)`
- `y` - array-like with shape `(n_instances,)` with instance labels
- `cv` - cross-validation generator responsible for creating *k*-fold splitting of `X` and `y`
> see the docs for info regarding the optional parameters

In each CV iteration, the estimator is fitted on training fold and class probabilities are predicted for instances 
within the test fold. Then, ROC and PR curves are generated from the probabilities.

The figure consists of:
- individual ROC/PR curves
- mean ROC/PR curve
- shaded region denoting +-1 std. dev.

Areas under ROC and PR curves are reported in the legend.

*Note:* Use the functions `draw_roc_cv` or `draw_prc_cv` to draw ROC or PR curves only 

## Learning curve

TODO - not yet implemented

Create plot showing performance evaluation for different sizes of training data. The method should accept: 
- existing `Axes`
- performance measure (e.g. accuracy, MSE, precision, recall, etc.)
- ...

## Correlation heatmap

TODO - not yet implemented

Grid where each square has a color denoting strength of a correlation between predictors. You can choose between Pearson and Spearman correlation coefficient, the result is shown inside the square. 

