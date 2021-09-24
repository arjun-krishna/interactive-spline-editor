import numpy as np

def linear_interpolation_at_t(p0, p1, t):
    return (1-t)*p0 + t*p1

def linear_interpolation_of_points(control_points):
    interpolated_points = list()
    time_array = np.linspace(0.0, 1.0, 101)
    if (control_points.shape[0] < 2): # need atleast two points to interpolate
        return interpolated_points
    for p0, p1 in zip(control_points[:-1], control_points[1:]):
        points = [linear_interpolation_at_t(p0, p1, t) for t in time_array]
        interpolated_points += points
    
    return np.array(interpolated_points)

def bezier_interpolation_at_t(p0, p1, p2, p3, t):
  """All the points are given as np.array. t is a floating number that represents time."""
  Mb = np.array([[-1, 3, -3, 1],[3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
  Gb = np.vstack((p0, p1, p2, p3))
  T = np.array([t**3, t**2, t, 1])
  return T @ Mb @ Gb

def bezier_interpolation_of_points(control_points):
  """control_points is a list of points (np.array)."""
  interpolated_points = list()  # The container for interpolated points
  time_array = np.linspace(0.0, 1.0, 101)  # time[0] = 0.0, time[1] = 0.01, ... time[100] = 1.0

  # For each segment of control points
  for i in range(0, control_points.shape[0], 3):
    if i + 3 >= control_points.shape[0]: # if out of range
      break
    p0, p1, p2, p3 = [control_points[idx] for idx in (i, i+1, i+2, i+3)]
    # Compute the interpolated points and append to the list
    points = [bezier_interpolation_at_t(p0, p1, p2, p3, t) for t in time_array]
    interpolated_points += points
  
  return np.array(interpolated_points)

def bspline_interpolation_at_t(p0, p1, p2, p3, t):
  """All the points are given as np.array. t is a floating number that represents time."""
  Mbs = np.array([[-1, 3, -3, 1],[3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6
  Gbs = np.vstack((p0, p1, p2, p3))
  T = np.array([t**3, t**2, t, 1])
  return T @ Mbs @ Gbs
  
def bspline_interpolation_of_points(control_points):
  """control_points is a list of points (np.array)."""
  interpolated_points = list()  # The container for interpolated points
  time_array = np.linspace(0.0, 1.0, 101)  # time[0] = 0.0, time[1] = 0.01, ... time[100] = 1.0

  # For each segment of control points (De Boor points)
  for i in range(control_points.shape[0]-3):
    p0, p1, p2, p3 = [control_points[idx] for idx in (i, i+1, i+2, i+3)]
    # Compute the interpolated points and append to the list
    points = [bspline_interpolation_at_t(p0, p1, p2, p3, t) for t in time_array]
    interpolated_points += points
  
  return np.array(interpolated_points)

def bspline_interpolation_of_points_v2(control_points):
  # ghost points (interpolating first and last)
  if control_points.shape[0] < 2:
      return []
  gp1 = 2*control_points[0,:] - control_points[1,:]
  gp2 = 2*control_points[-1,:] - control_points[-2,:]
  cps = np.vstack((gp1, control_points, gp2))
  return bspline_interpolation_of_points(cps) # reuse v1 implementation

def catmullrom_interpolation_at_t(p0, p1, p2, p3, t):
  """All the points are given as np.array. t is a floating number that represents time."""
  Mc = np.array([[-1, 3, -3, 1],[2, -5, 4, -1], [-1, 0, 1, 0], [0, 2, 0, 0]]) / 2
  Gc = np.vstack((p0, p1, p2, p3))
  T = np.array([t**3, t**2, t, 1])
  return T @ Mc @ Gc
  
def catmullrom_interpolation_of_points(control_points):
  """control_points is a list of points (np.array)."""
  interpolated_points = list()  # The container for interpolated points
  time_array = np.linspace(0.0, 1.0, 101)  # time[0] = 0.0, time[1] = 0.01, ... time[100] = 1.0

  # For each segment of control points
  for i in range(control_points.shape[0]-3):
    p0, p1, p2, p3 = [control_points[idx] for idx in (i, i+1, i+2, i+3)]
    # Compute the interpolated points and append to the list
    points = [catmullrom_interpolation_at_t(p0, p1, p2, p3, t) for t in time_array]
    interpolated_points += points
  
  return np.array(interpolated_points)

def c2_interpolation_of_points(control_points):
  # hard
  # big linear system and solve (invert lin-system server from numpy lib)
  if control_points.shape[0] < 2:
      return []
  N = control_points.shape[0]
  dim = control_points.shape[1]
  A = np.zeros((N, N))
  A[0,:2] = np.array([2, 1])
  for i in range(1,N-1):
    A[i,i-1:i+2] = np.array([1, 4, 1])
  A[-1,-2:] = np.array([1, 2])
  b = np.vstack((3*(control_points[1,:] - control_points[0,:]),    # boundary start
                 3*(control_points[2:,:] - control_points[:-2,:]), # middle derivatives
                 3*(control_points[-1,:] - control_points[-2,:]))) # boundary end
  D = np.linalg.inv(A) @ b
  cps = np.empty((3*N - 2, dim), dtype=control_points.dtype) # N points ( 2(N-1) + N = 3N - 2)
  # C0, D0', D1', C1, D1', D2', C2
  cps[0::3] = control_points
  cps[1::3] = control_points[:-1,:] + D[:-1,:]/3  # D1 = 3 ( C2 - C1) --> C2 = C1 + D1/3
  cps[2::3] = control_points[1:,:] - D[1:,:]/3 # D4 = 3 ( C4 - C3) --> C3 = C4 - D4/3
  return bezier_interpolation_of_points(cps)