import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import argparse

n = 8 #length and width of image
def sym_diag_grid(n,ratio = 0.5,k = 1):
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

def save_exact_size_PIL(n_grids, size = 8, vert_vlip = False, save_npz = False):
    #Create all grids 
    all_grids = np.zeros((n_grids, size, size), dtype=int)
    saved_files = []
    
    #Create save directory
    save_dir = os.path.join(os.getcwd(), "binary_grids_test1")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Files saved in: {save_dir}")
    for i in range(n_grids): 
        all_grids[i] = sym_diag_grid(8)

    if vert_vlip: 
        all_grids[n_grids//2:] = np.flip(all_grids[n_grids//2:], axis = 0)
    
    if save_npz: 
        npz_filename = (os.path.join(save_dir, "binary_grid_test.npz"))
        np.savez(npz_filename, (all_grids*255).astype(np.uint8))
        saved_files.append(npz_filename)

    
    else: 
        for i, grid in enumerate(all_grids):
            img = Image.fromarray((grid * 255).astype(np.uint8))
            if img.size != (64, 64):
                img = img.resize((64, 64), Image.Resampling.NEAREST)
            filename = os.path.join(save_dir, f'binary_grid_{i:03d}.jpg')
            img.save(filename, quality=95)
            saved_files.append(filename)

    return {
    'directory': save_dir,
    'files_saved': saved_files,
    'number_of_images': n_grids,
    'Vertical flip': vert_vlip,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_grids", type = int, default = 50, help = "Number of grids you want to generate")
    parser.add_argument("--size", type = int, default = 8, help = "grid size definer (so this is an 8x8 grid)")
    parser.add_argument("--hor_flip", action = "store_true", help = "If you want grids also mirrored vertically., default true")
    parser.add_argument("--save_npz", action = "store_true", help = "Save your images as a test.npz")
    parser.add_argument("--show_example", action = "store_true", help = "Show an example of the grid")
    args = parser.parse_args()

    if args.show_example: 
        A = sym_diag_grid(8, 0.8)
        print(A)
        plt.imshow(A,cmap='binary')
        plt.show()
    else:
        save_exact_size_PIL(args.n_grids, size = args.size, save_npz = args.save_npz, vert_vlip = args.hor_flip)
    
