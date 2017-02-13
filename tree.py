from sklearn import tree
from sklearn import datasets
from IPython.display import Image
import pydotplus
# X=[[1,0,0,0,0],[0,3,0,0,0],[0,0,4,0,0],[0,0,3,0,1],[2,1,1,0,1],[2,1,1,2,2],[2,1,2,0,1],[2,1,2,2,2],[2,1,3,0,2],[2,1,3,0,3],
#    [2,2,1,0,1],[2,2,2,0,1],[2,2,2,0,2],[2,2,2,0,3],[3,1,1,0,1],[3,1,2,0,1],[3,1,2,2,2],[3,1,3,0,2],[3,1,3,0,3],[3,2,1,0,1],
#    [3,2,2,0,1],[3,2,3,0,2],[2,1,1,1,2],[2,1,1,0,3],[2,1,2,1,2],[2,1,2,0,3],[2,2,1,0,2],[2,2,1,2,3],[2,2,2,0,2],[2,2,1,2,3],
#    [3,1,1,0,2],[3,1,1,0,3],[3,1,2,1,2],[3,1,2,0,3],[3,2,1,2,2],[3,2,2,2,2],[3,2,2,0,3],[2,2,1,1,3],[3,2,2,1,3],[3,2,1,1,2],
#    [3,2,1,0,3],[3,2,2,1,2],[3,2,2,0,3]]
# Y= [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3]
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(X, Y)
# dot_data = tree.export_graphviz(clf, out_file=None,
#                                 feature_names=['a','b','c','d','e'],
#                                 class_names=['0','1','2','3'],
#                                 filled=True, rounded=True,
#                                 special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_data)
# Image(graph.create_png())
iris = datasets.load_iris()
clf = tree.DecisionTreeClassifier()
clf2 = clf.fit(iris.data, iris.target)
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf2, out_file=f)
import os
os.unlink('iris.dot')
import pydotplus
with open("test.dot",'w') as f2:
    dot_data = tree.export_graphviz(clf2, out_file=None)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("iris.pdf")
    from IPython.display import Image
    dot_data = tree.export_graphviz(clf2,out_file=f2,
                             feature_names=iris.feature_names,
                             class_names=iris.target_names,
                             filled=True, rounded=True,
                             special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    Image(graph.create_png())
    pass
