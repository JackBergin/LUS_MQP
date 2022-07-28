# ============================================================
# file name: DP_SMPL_test.py
# ============================================================
"""
find points on SMPL model and RGB image given UV coord
"""
import cv2
import pickle
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

import detectron.utils.densepose_methods as dp_utils


def smpl_view_set_axis_full_body(ax, azimuth=0):
  # Manually set axis
  ax.view_init(0, azimuth)
  max_range = 0.55
  ax.set_xlim(-max_range, max_range)
  ax.set_ylim(-max_range, max_range)
  ax.set_zlim(-0.2-max_range, -0.2+max_range)
  ax.axis('off')


def smpl_view_set_axis_chest(ax, elevation=30, azimuth=0):
  # Manually set axis
  ax.view_init(elevation, azimuth)
  max_range = 0.28
  ax.set_xlim(-max_range, max_range)
  ax.set_ylim(-max_range, max_range)
  ax.set_zlim(0.15-max_range, 0.15+max_range)
  ax.axis('off')


def selected_uv2pix_in_image(IUV, U, V):
  '''
  calculate pixel position in RGB image given selected IUV & uv
  '''
  x_ = np.zeros(U.shape, dtype=int)
  y_ = np.zeros(U.shape, dtype=int)
  for i, (uu, vv) in enumerate(zip(U, V)):
    u2xy = np.where(IUV[:, :, 1] == uu)
    v2xy = np.where(IUV[:, :, 2] == vv)
    x_intersects = [x for x in u2xy[1] if x in v2xy[1]]
    y_intersects = [y for y in u2xy[0] if y in v2xy[0]]
    if len(x_intersects) <= 0 or len(y_intersects) <= 0:
      x_[i] = -1
      y_[i] = -1
    else:
      x_[i] = np.mean(x_intersects)
      y_[i] = np.mean(y_intersects)
    print("iter:", i, "row: ", x_[i], "col:", y_[i])
  return x_, y_


def selected_uv2pnt_on_surface(DP, U, V, face_idx=2):
  '''
  calculate points on SMPL given selected uv
  '''
  collected_x = np.zeros(U.shape)
  collected_y = np.zeros(U.shape)
  collected_z = np.zeros(U.shape)
  for i, (uu, vv) in enumerate(zip(U, V)):
    print("iter: ", i, "u: ", uu, "v: ", vv)
    # uses modified methods for faster processing
    FaceIndex, bc1, bc2, bc3 = DP.IUV2FBC_fast(face_idx, uu/255., vv/255.)
    # Use FBC to get 3D coordinates on the surface.
    p = DP.FBC2PointOnSurface(FaceIndex, bc1, bc2, bc3, Vertices)
    collected_x[i] = p[0]
    collected_y[i] = p[1]
    collected_z[i] = p[2]
  return collected_x, collected_y, collected_z


def colorize_person(RGB, IUV, face_idx=2):
  '''
  get person color for scatter plot
  '''
  if face_idx != 0:
    pcolor = RGB[np.where(IUV[:, :, 0] == face_idx)]
  else:
    pcolor = RGB[np.where(IUV[:, :, 0] > 0)]
  return pcolor


# Now read the smpl model.
with open('../DensePoseData/basicmodel_m_lbs_10_207_0_v1.0.0.pkl', 'rb') as f:
  data = pickle.load(f)
  Vertices = data['v_template']  # Loaded vertices of size (6890, 3)
  X, Y, Z = [Vertices[:, 0], Vertices[:, 1], Vertices[:, 2]]

DP = dp_utils.DensePoseMethods()

RGB = cv2.imread('../DensePoseData/image_buffer/incoming.png')
IUV = cv2.imread('../DensePoseData/infer_out/incoming_IUV.png')
RGB = cv2.cvtColor(RGB, cv2.COLOR_BGR2RGB)

# get chest area
IUV_chest = np.zeros((IUV.shape))
chest_idx = np.where(IUV[:, :, 0] == 2)
IUV_chest[chest_idx] = IUV[chest_idx]

# Convert IUV to FBC (faceIndex and barycentric coordinates.)
isComputeAll = False
U_chest = IUV_chest[:, :, 1].flatten()
V_chest = IUV_chest[:, :, 2].flatten()
U_chest_tar = np.array([255/2-38, 255/2-38, 255/2-78, 255/2-78,   # anterior
                        255/2-20, 255/2-20, 255/2-65, 255/2-65], dtype=int)  # lateral
V_chest_tar = np.array([255/2-30, 255/2+30, 255/2-30, 255/2+30,   # anterior
                        255/2-80, 255/2+80, 255/2-80, 255/2+80], dtype=int)  # lateral

# U_chest_tar = np.array([60, 100, 60, 100])
# V_chest_tar = np.array([155, 155, 105, 105])

print("find pix in image from uv")
x_, y_ = selected_uv2pix_in_image(IUV_chest, U_chest_tar, V_chest_tar)
print("find points on SMPL from uv")
if isComputeAll:
  U_chest_pick = U_chest[np.where(U_chest != 0)]
  V_chest_pick = V_chest[np.where(V_chest != 0)]
else:
  U_chest_pick = U_chest_tar
  V_chest_pick = V_chest_tar
collected_x, collected_y, collected_z = selected_uv2pnt_on_surface(DP, U_chest_pick, V_chest_pick)

pcolor = RGB[np.where(IUV[:, :, 0] == 2)]

fig = plt.figure(figsize=[15, 5])

# Visualize the image and collected points.
ax = fig.add_subplot(121)
ax.imshow(RGB)
ax.scatter(x_, y_, s=30, c=np.arange(len(U_chest_tar)), cmap=cm.jet)
plt.title('Points on the image')
ax.set_xlim(0, RGB.shape[1])
ax.set_ylim(0, RGB.shape[0])
ax.invert_yaxis()
ax.axis('off')

# Visualize the full body smpl male template model and collected points
ax = fig.add_subplot(122, projection='3d')
ax.scatter(Z, X, Y, s=0.05, c='k')
if isComputeAll:
  ax.scatter(collected_z, collected_x, collected_y, s=5, c=pcolor/255.)
else:
  ax.scatter(collected_z, collected_x, collected_y, s=30, c=np.arange(len(U_chest_pick)), cmap=cm.jet)
smpl_view_set_axis_chest(ax)
plt.title('Points on the SMPL model')

#
plt.show()
