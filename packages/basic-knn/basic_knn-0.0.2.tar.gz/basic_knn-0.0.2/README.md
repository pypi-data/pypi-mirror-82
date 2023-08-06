# KNN Algorithm Module

### What is KNN?
In k-NN classification, the output is a class membership. An object is classified by a plurality vote of its neighbors, with the object being assigned to the class most common among its k nearest neighbors (k is a positive integer, typically small). If k = 1, then the object is simply assigned to the class of that single nearest neighbor.

k-NN is a type of instance-based learning, or lazy learning, where the function is only approximated locally and all computation is deferred until function evaluation. Since this algorithm relies on distance for classification, normalizing the training data can improve its accuracy dramatically. 

(Wikipedia Article about KNN, https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)

### How to Install?
It is always better to use "pip" (Package manager for Python).
```
pip install basic_knn
```

### Sample Usage

#### Create Model
```
# import knn classifier
from basic_knn import KNNClassifier

# sample data
data_x = [...]
data_y = [...]
labels = [...]

# create model
model = KNNClassifier(xs = xs, ys = ys, labels = labels)
```

#### Make Predictions
```
# sample input for predictions
sample_input = (..., ...)

# make prediction
model.predict(sample_input)
```