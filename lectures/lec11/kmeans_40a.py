# kmeans_40a.py
# Author: Suraj Rampure, fa21 (adapted from existing code in DSC 40A)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

class kMeans:
    def __init__(self, X, k, num_iters=50, distance_metric=None, initial_centroids=None, seed=None):
        
        if seed:
            np.random.seed(seed)
        
        self.X = X
        self.k = k
        self.num_iters = num_iters
        
        if distance_metric is None:
            self.distance_metric = self.squared_distance
        else:
            self.distance_metric = distance_metric

        
        self.current_iter = 0
        
        # dim 1: iteration
        # dim 2: k
        # dim 3: data points
        self.centroid_history = np.zeros((self.num_iters + 1, self.k, self.X.shape[1]))
        
        if initial_centroids is None:
            self.initial_centroids = self.generate_initial_centroids()
        else:
            self.initial_centroids = initial_centroids
            
        self.current_centroids = self.initial_centroids
        
        self.centroid_history[self.current_iter, :, :] = self.current_centroids
        
        # One row per data point, one column per iteration tracking the group per iteration
        self.group_history = np.zeros((self.X.shape[0], self.num_iters + 1))
        
        self.current_groups = self.update_groups()
        
# #         self.group_history[:, self.current_iter] = self.current_groups
        
        self.current_iter += 1
        
        # For visualization purposes
        
        self.color_map = {
            '1': 'red',
            '2': 'blue',
            '3': 'green',
            '4': 'gold',
            '5': 'purple',
            '6': 'orange',
            '7': 'pink'
        }
        
    def generate_initial_centroids(self):
        return self.X.sample(self.k).values
        
    def squared_distance(self, x, centroid):
        """Computes the squared distance between a data point x and a centroid."""
        return np.sum((x - centroid)**2)
    
    def absolute_distance(self, x, centroid):
        '''Computes the absolute distance between a data point x and a centroid.'''
        return np.sum(np.abs(x - centroid))
    
    def cluster_cost(self, cluster, centroid):
        """Computes the total distance between all data points in a cluster and a centroid.
           Equivalent to the cost of that cluster/centroid combination.
        """
        return np.sum([distance_metric(x, centroid) for x in cluster])
    
    def find_closest_centroid(self, x):
        """Determines the index of the centroid closest to a given data point x."""
        smallest_distance = float('inf')
        best_centroid = self.current_centroids[0]
        for centroid in self.current_centroids:
            this_distance = self.distance_metric(x, centroid)
            if this_distance < smallest_distance:
                best_centroid = centroid
                smallest_distance = this_distance
        return np.where(self.current_centroids == best_centroid)[0][0] + 1
    
    def update_groups(self):
        self.current_groups = self.X[['x1', 'x2']].apply(self.find_closest_centroid, axis=1)
        self.group_history[:, self.current_iter] = self.current_groups
    
    def update_centroids(self):
        """Function that takes in a data matrix X, k, and an array of current cluster assignments and returns an array of centroids."""
        new_centroids = np.zeros((self.k, 2))
        X_with_clusters = self.X.copy()
        X_with_clusters['current_cluster'] = self.current_groups
        for cluster in np.arange(1, self.k+1):
            cluster_only = X_with_clusters.loc[X_with_clusters['current_cluster'] == cluster, ['x1', 'x2']]
            new_centroid = cluster_only.mean().values
            new_centroids[cluster - 1] = new_centroid
        self.current_centroids = new_centroids
        self.centroid_history[self.current_iter, :, :] = self.current_centroids
        
    def one_iteration(self):
        self.update_groups()
        self.update_centroids()
        self.current_iter += 1
    
    def iterate(self):
        for _ in range(self.num_iters):
            self.one_iteration()
            
    def inertia(self):
        assert self.current_iter == self.num_iters + 1, 'You must call .iterate() before calling .inertia().'
        total = 0
        X_with_clusters = self.X.copy()
        X_with_clusters['current_cluster'] = self.current_groups
        for i in range(X_with_clusters.shape[0]):
            group = X_with_clusters['current_cluster'].astype(int).iloc[i]
            centroid = self.current_centroids[group - 1]
            total += self.distance_metric(X_with_clusters.iloc[i, :-1].values, centroid)
        return total
            
    def create_centroid_animation(self):
        df = pd.DataFrame(self.centroid_history.reshape(((self.num_iters + 1) * self.k, self.X.shape[1])))
    
        # Crucial: this assumes the groups go [1, 2, 3, 1, 2, 3, etc. which they do]
        df['cluster'] = list(np.arange(1, self.k+1).astype(str)) * (self.num_iters + 1)
        df['iter'] = np.repeat(np.arange(0, self.num_iters + 1), self.k)
        return px.scatter(df, x=0, y=1, 
                          color='cluster', 
                          animation_frame='iter', 
                          size=np.ones(df.shape[0]), size_max=25,
                          range_x = [self.X['x1'].min() - 1, self.X['x1'].max() + 1],
                          range_y = [self.X['x2'].min() - 1, self.X['x2'].max() + 1],
                          color_discrete_map = self.color_map,
                          labels={0: 'x1', 1: 'x2'})
    
    def create_group_animation(self):
        df = self.X.copy()
        df = pd.DataFrame(list(df.values) * (self.num_iters + 1))
        df['cluster'] = self.group_history.T.flatten().astype(int).astype(str)
        df['iter'] = np.repeat(np.arange(0, self.num_iters + 1), self.X.shape[0])
    #     return df
        return px.scatter(df, x=0, y=1, 
                          color='cluster', 
                          animation_frame='iter', 
                          size=np.ones(df.shape[0]), size_max=9,
                          range_x = [self.X['x1'].min() - 1, self.X['x1'].max() + 1],
                          range_y = [self.X['x2'].min() - 1, self.X['x2'].max() + 1],
                          color_discrete_map = self.color_map)
    
    def show_full_animation(self):
        if self.current_iter != self.num_iters + 1:
            self.iterate()
        s1 = self.create_centroid_animation()
        s2 = self.create_group_animation()
        
        frames = [
            go.Frame(data=s2.frames[i].data + s1.frames[i].data, name=s1.frames[i].name)
            for i in range(len(s1.frames))
        ]

        # increase duration as contour takes a while to redraw
        # increase duration as contour takes a while to redraw
        # updmenus = [{"args": [None, {"frame": {"duration": 1500}}],"label": "&#9654;","method": "animate",},
        #             {'args': [[None], {'frame': {'duration': 0}, 'mode': 'immediate', 'fromcurrent': True, }],
        #                   'label': '&#9724;', 'method': 'animate'} ]

        # now can animate...
        fig = go.Figure(data=frames[0].data, frames=frames, layout=s1.layout)#
        fig.update_xaxes(title='x1')
        fig.update_yaxes(title='x2')
        fig.update_layout(width=800, height=600, showlegend=False)
        return fig