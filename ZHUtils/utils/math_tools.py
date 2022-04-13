import numpy as np

def surrounding_2Dpos (radius, num_split, sorted_type='ascending'):
    """
    Args:
        radius: max radius of point relative to center
        num_split: number of splits on one axis
        sorted_type: from centor to bound use 'ascending'
    """
    x = np.linspace(-radius, radius, num_split)
    y = np.linspace(-radius, radius, num_split)
    xv, yv = np.meshgrid(x, y)

    coord_pairs = list(zip(xv.flatten(), yv.flatten()))
    
    if sorted_type == 'ascending':
        out_pairs = sorted(coord_pairs, key=lambda z: z[0]**2 + z[1]**2 )
        out_pairs = coord_pairs[:len(coord_pairs)//2] \
            + [pair for pair in coord_pairs[len(coord_pairs)//2:] if pair[1]**2 + pair[0]**2 <= radius**2 ]
    else:
        raise NotImplementedError()
    return out_pairs

def surrounding_3Dpos(radius, num_split=None, sorted_type='ascending'):
    """
    Args:
        radius: max radius of point relative to center
        num_split: number of splits on one axis
        sorted_type: from centor to bound use 'ascending'
    """
    if num_split is None:
        num_split = 2*int(radius) + 1
    x = np.linspace(-radius, radius, num_split)
    y = np.linspace(-radius, radius, num_split)
    z = np.linspace(-radius, radius, num_split)
    xv, yv, zv = np.meshgrid(x, y, z)

    coord_pairs = list(zip(xv.flatten(), yv.flatten(), zv.flatten()))
    
    if sorted_type == 'ascending':
        out_pairs = sorted(coord_pairs, key=lambda k: k[0]**2 + k[1]**2 + k[2]**2 )
        out_pairs = coord_pairs[ : int(len(coord_pairs) * 0.52)+1] # 0.52 ratio of points is inside the sphere
    else:
        raise NotImplementedError()
    return out_pairs

def euclidean_distance(
    pos_a, pos_b
) -> float:
    return np.linalg.norm(np.array(pos_b) - np.array(pos_a), ord=2)


def scaling(bound, target_range, value):
    """
    Scaling a value from a range (bound) to a target_range
    """
    value = np.clip(value, bound[0], bound[1])
    v_std = (value-bound[0]) / (bound[1]-bound[0])
    return v_std * (target_range[1] - target_range[0]) + target_range[0]

def connect2D(point1, point2):
    """ 
    Connecting two points by sampling locations between them
    Args:
        point1: start point
        point2: end point to be connected
    """
    ends = [point1, point2]
    d0, d1 = np.abs(np.diff(ends, axis=0))[0]
    if d0 > d1: 
        return np.c_[np.linspace(ends[0, 0], ends[1, 0], d0+1, dtype=np.int32),
                     np.round(np.linspace(ends[0, 1], ends[1, 1], d0+1))
                     .astype(np.int32)]
    else:
        return np.c_[np.round(np.linspace(ends[0, 0], ends[1, 0], d1+1))
                     .astype(np.int32),
                     np.linspace(ends[0, 1], ends[1, 1], d1+1, dtype=np.int32)]
