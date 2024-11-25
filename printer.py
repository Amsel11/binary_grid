import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

n = 8 #length and width of image
def sym_diag_grid(n,ratio,k = 1):
    #Creates a grid which is transpose invariant. 
    matrix = np.zeros((n,n), dtype=int)
    upper_triangle = np.triu_indices(n, k) 
    matrix[upper_triangle] = np.random.choice([0, 1], size=len(upper_triangle[0]),p = [1-ratio,ratio])
    A = matrix + matrix.T
    return  A

A = sym_diag_grid(n,0.8)
print (A)
plt.imshow(A, cmap = 'binary')
plt.axis('off')

def save_exact_size_PIL(n_grids):
    save_dir = os.path.join(os.getcwd(), "binary_grids_2")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    print(f"Files saved in: {save_dir}")

    for i in range(n_grids):
        grid = sym_diag_grid(n,0.6)
        img_array = (grid * 255).astype(np.uint8)
        img = Image.fromarray(img_array)
        
        # Verify/force size to be 64x64
        if img.size != (64, 64):
            img = img.resize((64, 64), Image.Resampling.NEAREST)
        
        filename = os.path.join(save_dir, f'binary_grid_{i:03d}.jpg')
        img.save(filename, quality=95)
        
        # Verify saved image size
        saved_img = Image.open(filename)
        print(f"Image {i} size: {saved_img.size}")

grids = save_exact_size_PIL(200)
