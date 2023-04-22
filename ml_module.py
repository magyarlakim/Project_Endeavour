"""
This module contains all the custom made classes and functions for the ML projects
"""
import sklearn
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#visually displaying results
import matplotlib.pyplot as plt
from sklearn import tree

#Classes
class GenModelClass:
    def __init__(self, DatasetInput):
        self.DatasetInput=DatasetInput
        print("initializing parameters...")
    
    def load_target_and_dataset(self):
        """Identify the data and the target population from the dataset

        Args:
            None

        Returns:
            data: obj
                Data on which the model will ned to be run
            target: obj
                Data which contains the target outputs
            target_names: obj
                Data which contains the target outputs names

        """
        self.data = self.DatasetInput.data
        self.target = self.DatasetInput.target
        self.target_names = self.DatasetInput.target_names
        return [self.data, self.target, self.target_names]

class DimensionalityReductionClass(GenModelClass):
    """ The DimensionalityReduction class loads in a basic dataset class 
    represent a data for which dimesnionaloty reduction will be performed:
    ...

    Attributes
    ----------
    DatasetInput : array
        Array on which the dimensionaity reduction exercise will be perfomed

    Methods
    -------
    load_target_and_dataset():
        Prints the person's name and age.
    pca_lda_model(isPCA:bool=True, n_components=2):
        specify the model using the number of components and isPCA boolean variable as input
    model_fitting(model):
        fit the model to the database defined at instantiation of the class and produce results
    """

    def pca_lda_model(self, isPCA:bool=True, n_components=2):
        """A module that is performing the creation and parametrization of the model.

        Args:
            isPCA (bool, optional): _description_. Defaults to True.
            n_components (int, optional): _description_. Defaults to 2.

        Returns:
            model(scikit-learn model class): a fully fledged model ready to be fit to the population
        """
        if (isPCA):
            model = PCA(n_components=n_components)
        else:
            model = LinearDiscriminantAnalysis(n_components=n_components)
        return model
    
    def model_fitting(self, model):
        """This function performs the fitting of the model to the predefined dataset

        Args:
           model(scikit-learn model class): a fully fledged model ready to be fit to the population

        Returns:
            The results of the fitted model to the dataset
        """
        if isinstance(model, sklearn.discriminant_analysis.LinearDiscriminantAnalysis):
            results=model.fit(self.data, self.target)
        else:
            results=model.fit(self.data)
        return results
    
class ClusteringClass(GenModelClass):
    """ The Clustering class loads in a basic dataset class
    and performs multiple different clustering operations on it
    """ 
        
    def clustering_model(self, no_of_clusters=3, MiniBatch: bool=False,batch_size=1000):
        """A module that is performing the creation and parametrization of the model.

        Args:
            no_of_clusters (int, optional): _description_. Defaults to 3.
            MiniBatch (bool, optional): _description_. Defaults to False.
            batch_size (int, optional): _description_. Defaults to 1000.

        Returns:
            model(scikit-learn model class): a fully fledged model ready to be fit to the population
        """
        self.n_clusters = no_of_clusters
        if (MiniBatch):
            model = MiniBatchKMeans(n_clusters=3, n_init="auto",batch_size=batch_size)
        else:
            model = KMeans(n_clusters=3, n_init="auto")
        return model

    def model_fitting(self, model):
        """This function performs the fitting of the model to the predefined dataset

        Args:
           model(scikit-learn model class): a fully fledged model ready to be fit to the population

        Returns:
            The results of the fitted model to the dataset
        """
        if isinstance(model, sklearn.discriminant_analysis.LinearDiscriminantAnalysis):
            results=model.fit(self.data, self.target)
        else:
            results=model.fit(self.data)
        return results

class DecisionTree(GenModelClass):
    """Class tro generate decision tree related outputs

    Args:
        GenModelClass (class): Inheritance from General Model class
    """
    def model_specification(self, Modeltype: str="Decision_tree"):
        self.Modeltype=Modeltype
        if (Modeltype=="Decision_tree"):
            model = tree.DecisionTreeClassifier()
        else:
            model = tree.DecisionTreeClassifier()
        return model

    def model_fitting(self, model):
        """This function performs the fitting of the model to the predefined dataset

        Args:
           model(scikit-learn model class): a fully fledged model ready to be fit to the population

        Returns:
            The results of the fitted model to the dataset
        """
        if (56 == "faulty"):
            results=model.fit(self.data, self.target)
        else:
            results=model.fit(self.data, self.target)
        return results

    def visualization(self):
            model = self.model_specification(Modeltype = "Decision_tree")
            fitted_model = self.model_fitting(model)
            outputTree = tree.plot_tree(fitted_model)
            return fitted_model, outputTree