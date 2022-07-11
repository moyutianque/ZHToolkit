import trimesh
from trimesh.voxel.creation import voxelize


if __name__ == '__main__':

  import numpy as np
  import matplotlib.pyplot as plt
  import time

  vertices = np.array([[-10,-10,-10], [3,3,-10], [3, -10, -10], [10,10,10]])
  triangles = np.array([
          [0, 1, 2], 
          [0, 2, 3],
          [0, 1, 3],
          # [1, 2, 3]
      ]
  )
  tic = time.time()

  # Trimesh solution
  mesh = trimesh.Trimesh(vertices, triangles)
  voxels = voxelize(mesh, pitch=1)
  points_inner = voxels.points
  print(f"{time.time()-tic: .4f} seconds")
  import ipdb;ipdb.set_trace() # breakpoint 51

  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1, projection='3d')

  ax.scatter(points_inner[:,0], points_inner[:,1], points_inner[:,2], color='black', marker='o')
  for tri in triangles:
      points = np.array([vertices[tri[0]], vertices[tri[1]], vertices[tri[2]], vertices[tri[0]]])
      ax.plot(points[:,0], points[:,1], points[:,2])

  plt.show()
