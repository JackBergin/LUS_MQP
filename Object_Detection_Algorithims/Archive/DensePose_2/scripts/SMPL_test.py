# ============================================================
# file name: SMPL_test.py
# ============================================================
"""
test SMPL model visualization
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
import pickle

with open('DensePoseData/basicmodel_m_lbs_10_207_0_v1.0.0.pkl', 'rb') as f:
  data = pickle.load(f)
  Vertices = data['v_template']  # Loaded vertices of size (6890, 3)
  X, Y, Z = [Vertices[:, 0], Vertices[:, 1], Vertices[:, 2]]


def smpl_view_set_axis_full_body(ax, azimuth=0):
  # Manually set axis
  ax.view_init(0, azimuth)
  max_range = 0.55
  ax.set_xlim(- max_range,   max_range)
  ax.set_ylim(- max_range,   max_range)
  ax.set_zlim(-0.2 - max_range,   -0.2 + max_range)
  ax.axis('off')


def smpl_view_set_axis_face(ax, azimuth=0):
  # Manually set axis
  ax.view_init(0, azimuth)
  max_range = 0.1
  ax.set_xlim(- max_range,   max_range)
  ax.set_ylim(- max_range,   max_range)
  ax.set_zlim(0.45 - max_range,   0.45 + max_range)
  ax.axis('off')


# Now let's rotate around the model and zoom into the face.
fig = plt.figure(figsize=[16, 4])

ax = fig.add_subplot(141, projection='3d')
ax.scatter(Z, X, Y, s=0.02, c='k')
smpl_view_set_axis_full_body(ax)

ax = fig.add_subplot(142, projection='3d')
ax.scatter(Z, X, Y, s=0.02, c='k')
smpl_view_set_axis_full_body(ax, 45)

ax = fig.add_subplot(143, projection='3d')
ax.scatter(Z, X, Y, s=0.02, c='k')
smpl_view_set_axis_full_body(ax, 90)

ax = fig.add_subplot(144, projection='3d')
ax.scatter(Z, X, Y, s=0.2, c='k')
smpl_view_set_axis_face(ax, -40)

plt.show()
