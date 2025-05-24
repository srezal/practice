import numpy as np

int_ = (int, np.int_, np.int8, np.int16, np.int32, np.int64)
float_ = float, np.float16, np.float32, np.float64
number_ = *int_, *float_
