import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import pandas as pd


class LocationPref:
    def __init__(self, campus_boundary, map_dict, map_locs):
        """
        Initialize Location Preference PDF

        Parameters:
        campus_boundary: tuple
            (x1, x2, y1, y2) defining coordinates of campus boundary
        map_dict: dict
            {location: [x_c, y_c]} defining the center points of each location
        map_locs: dict
            {location: [(x1, x2), (y1, y2)]} defining the coordinates of the boundary for each location
        """
        
        self.campus_boundary = campus_boundary
        self.grid_size = 100
        self.dict = map_dict
        self.locs = map_locs

        x1, x2, y1, y2 = campus_boundary
        x = np.linspace(x1, x2, self.grid_size)
        y = np.linspace(y1, y2, self.grid_size)
        self.X, self.Y = np.meshgrid(x, y)
        self.grid = np.dstack((self.X, self.Y))

    def create_pref_pdf(self, preferred_locs):
        """
        Create PDF using Gaussian Mixture Model for User Preferences over Grid

        Parameters:
        preferred_locs: list
            List of names of preferred locations
        """

        n_locs = len(preferred_locs)

        # get coords of preferred locs
        pref_locs_coords = []
        for i in preferred_locs:
            pref_locs_coords.append(self.dict[i])

        # get weights for each gaussian in gmm
        pref_strengths = [1.0] * n_locs
        total_strength = sum(pref_strengths)
        weights = [s / total_strength for s in pref_strengths]

        spreads = [0.15] * n_locs

        # define mean, weight, cov and then get gmm 
        pref_dist = np.zeros_like(self.X)
        for i in range(n_locs):
            mean = pref_locs_coords[i]
            weight = weights[i]
            cov = np.eye(2) * spreads[i]

            # create gaussian dist with mean and cov defined above 
            gaussian = multivariate_normal(mean=mean, cov=cov)
            pref_dist += weight * gaussian.pdf(self.grid)

        # normalize to get pdf
        if np.sum(pref_dist) > 0:
            pdf = pref_dist / np.sum(pref_dist)
        
        # print("sum pref dist:", sum(sum(pdf)))
        
        return pdf
    

    def visualize(self, user_preference_distribution):
        """
        Visualize the campus map with user preferences
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        contour = ax.contourf(self.X, self.Y, user_preference_distribution, 
                             cmap='Blues', levels=50, alpha=0.7)
        fig.colorbar(contour, ax=ax, label='Probability Density')

        for label, (x, y) in self.dict.items():
            ax.text(x, y, label, fontsize=10, ha='center', va='center', color='black', fontweight='bold')
    
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        
        x1, x2, y1, y2 = self.campus_boundary
        ax.set_xlim(x1, x2)
        ax.set_ylim(y1, y2)
        
        plt.tight_layout()
        return fig, ax
    
    def probability_locs(self, pdf):
        """
        Get probability of each location from the PDF.
        Parameters:
        pdf: numpy array
            probability density function of the locations that the user prefers/is most likely to go to
        """
        loc_probs = np.zeros((self.campus_boundary[1], self.campus_boundary[3]))
        cell_area = 1

        for inds in (self.locs).values():
            x1 = inds[0][0]
            x2 = inds[0][1]
            y1 = inds[1][0]
            y2 = inds[1][1]
            mask = (self.X >= x1) & (self.X <= x2) & \
                (self.Y >= y1) & (self.Y <= y2)

            loc_probs[x1][y1] = np.sum(pdf[mask]) * cell_area
        
        # normalize to ensure probs sum to 1
        loc_probs = loc_probs / np.sum(loc_probs)

        return loc_probs
    

# if __name__ == "__main__":

#     campus_bounds = (0, 3, 0, 2)  
#     stanford_map_dict = {"ev": [0.5, 1.5], "gsb": [0.5, 0.5], "memchu": [1.5, 0.5], "tressider": [1.5, 1.5], "med": [2.5, 0.5], "engg": [2.5, 1.5]}
#     stanford_map_locs = {"ev": [(0, 1), (1, 2)], "gsb": [(0, 1), (0, 1)], "memchu": [(1, 2), (0, 1)], "tressider": [(1, 2), (1, 2)], "med": [(2, 3), (0, 1)], "engg": [(2, 3), (1, 2)]}

#     pref_locs = ["med", "memchu"]

#     pref_obj = LocationPref(campus_bounds, stanford_map_dict, stanford_map_locs)
    
#     pdf = pref_obj.create_pref_pdf(pref_locs)
    
#     fig, ax = pref_obj.visualize(pdf)
#     plt.show()

#     prob_locs = pref_obj.probability_locs(pdf)
#     print(sum(sum(prob_locs)))
#     print(prob_locs)