"""
This script is responsible for calculating concentration on a given entropy
"""
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from math import pi
import urllib
from time import perf_counter
print("Hello world")

class Paramount():
    """ A usefull class to start with
    :inpu1= Nothing
    :input2= Nothing again
    :outout= Nothing
    """
    language= 'Turkish'
    version='1.1'
    def say_hello():
        print(f'Hello from{Paramount.language}')


class Circle:
    """ This class is using property and cahcing the value """
    def __init__(self, radius):
        self._radius = radius
        self._area = None
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._area = None
        self._radius = value
    
    @property
    def area(self):
        if self._area is None:
            print('Calculating area')
            self._area = pi * (self.radius ** 2)
        return self._area


c= Circle(1)
c.area
c.radius = 2
c.__dict__
c.area

class WebPage:
    def __init__(self, url):
        self.url = url
        self._page= None
        self._load_time_secs = None
        self._page_size = None

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value
        self._page = None
    
    @property
    def page(self):
        if self._page is None:
            self.download_page()
        return self._page
    
    @property
    def page_size(self):
        if self._page is None:
            self.download_page()
        return self._page_size

    @property
    def time_elapsed(self):
        if self._page is None:
            self.download_page()
        return self._load_time_secs
    
    def download_page(self):
        self._page_size=None
        self._load_time_secs = None
        start_time = perf_counter()
        with urllib.request.urlopen(self.url) as f:
            self._page=f.read()
        end_time= perf_counter()
        self._load_time_secs= end_time- start_time

urls = [
    'https://wwww.google.com',
    'https://wwww.python.org',
    'https://wwww.yahoo.com'
]

for url in urls:
    page=WebPage(url)
    print(f'{url}\tsize={format(page.page_size, "_")}\telapsed={page.time_elapsed:.2f} secs')
    