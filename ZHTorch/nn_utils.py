import unittest

def conv2d_size_out(size_in: tuple, kernel_size, stride, padding):
    """
    Calculate output grid size of conv2d

    Args:
        size_in (Tuple): (feature_h, feature_w)
        kernel_size (int)
        stride (int)
        padding (int)

    Returns:
        Tuple: (new_feature_h, new_feature_w)
    """
    h = ((size_in[0] + 2 * padding - (kernel_size - 1) - 1) // stride ) + 1
    w = ((size_in[1] + 2 * padding - (kernel_size - 1) - 1) // stride ) + 1
    return (int(h),int(w))


class TestMethods(unittest.TestCase):
    def test_conv2d_size_out(self):
        size_in = (100,150)
        size_out = (int(48), int(73))
        self.assertEqual(
            size_out,
            conv2d_size_out(
                size_in, kernel_size=7, stride=2, padding=1
            )
        )

if __name__ == '__main__':
            
    unittest.main()
