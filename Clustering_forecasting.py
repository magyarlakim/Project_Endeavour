"""
This script demonstrates clustering and forecasting abilities using the scikit-learn package
and financial dataset using user defined tailor made packages
"""
import pandas as pd
import numpy as np
#stat analysis
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
#graphs
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
#import proprietary module
import Aux_functions as aux
import ml_module as ml_module
from importlib import reload
reload(ml_module)

#Load the dataset
MyInputData=load_iris()

# 1. Compare the result of Principal Component Analysis and Linear Discriminant Analysis visually
Dimension = ml_module.DimensionalityReductionClass(MyInputData)
X_data, Y, target_names = Dimension.load_target_and_dataset()

#PCA model
pca_model = Dimension.pca_lda_model(n_components=2,isPCA=True)
PCA = Dimension.model_fitting(pca_model)
X1 = PCA.transform(X_data)
# Percentage of variance explained for each components
print("explained variance ratio (first two components): %s"% str(PCA.explained_variance_ratio_))

#LDA model
lda_model = Dimension.pca_lda_model(n_components=2,isPCA=False)
LDA = Dimension.model_fitting(lda_model)
X2 = LDA.transform(X_data)

#plot the results on a graph
colors = ["#BB8FCE", "#3498DB", "#7F8C8D"]
title1="PCA of IRIS dataset"
title2="LDA of IRIS dataset"
mainTitle= 'PCA and LDA comparison'
ComparisonPlot=aux.comparison_scatter_plotting_duo(X1,X2,Y, target_names, colors, title1, title2, mainTitle, ShowPlot=True)


# 2. Compare the result of K-means and MiniBatchKMeans algorythm results
Clustering = ml_module.ClusteringClass(MyInputData)
X_data, Y_data, target_names = Clustering.load_target_and_dataset()
#Calibrate the models
Calibrated_models= {}
Calibrated_models['Model_batch_1K'] = Clustering.clustering_model(no_of_clusters=3, MiniBatch=True,batch_size=1000)
Calibrated_models['Model_batch_50'] = Clustering.clustering_model(no_of_clusters=3, MiniBatch=True,batch_size=50)
Calibrated_models['Model_Kmeans'] = Clustering.clustering_model(no_of_clusters=3, MiniBatch=False)

ModelList = ['Model_batch_1K','Model_batch_50','Model_Kmeans']
#Fit the models
Fitted_models= {}
Ordered_cluster_centers={}
Cluster_centers_labels = {}
for i, model in enumerate(ModelList):
    print("Fitting "+model+ " model..")   
    Fitted_models[model]=Clustering.model_fitting(Calibrated_models[model])
    
    #reorder cluster centers
    if (i==0):
        Ordered_cluster_centers[model] = Fitted_models[model].cluster_centers_
    else:
        order=pairwise_distances_argmin(Fitted_models[model].cluster_centers_,Fitted_models[ModelList[0]].cluster_centers_)
        Ordered_cluster_centers[model] = Fitted_models[model].cluster_centers_[order]

    #recalculate pairwise distances
    Cluster_centers_labels[model] = pairwise_distances_argmin(X_data,Ordered_cluster_centers[model])
    
    Ordered_cluster_centers[model][:,0]
    Ordered_cluster_centers[model][:,1]
    target_names

fig=px.scatter_3d(x=X_data[:,0],y=X_data[:,2],z=X_data[:,1],color=Y, size=X_data[:,3],title="Comparing KMeans and MiniBatch Clustering results")
for i, model in enumerate(ModelList):
    fig.add_trace(go.Scatter3d(x=Ordered_cluster_centers[model][:,0], y=Ordered_cluster_centers[model][:,2], z=Ordered_cluster_centers[model][:,1],  text="Centroid "+model, mode='markers', marker=dict(size=10, color=colors[i])))
fig.show()

# Section 3 Fitting and training a neural network
DecisionTree= ml_module.DecisionTree(MyInputData)
DecisionTree.load_target_and_dataset()
Treemodel,graph = DecisionTree.visualization()