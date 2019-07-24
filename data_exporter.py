import numpy as np
vertices = """
        -1.0f, -1.0f, 0.0f, 0.0f,
         1.0f,  1.0f, 1.0f, 1.0f,
        -1.0f,  1.0f, 0.0f, 1.0f,

        -1.0f, -1.0f, 0.0f, 0.0f,
         1.0f, -1.0f, 1.0f, 0.0f,
         1.0f,  1.0f, 1.0f, 1.0f
"""

def transform_array(str_):
    vertices_ = str_.replace("\n", "")
    vertices_ = vertices_.replace(" ", "")
    return np.array([float(i.replace("f", "")) for i in vertices_.split(",")], dtype=np.float32)


vertices = transform_array(vertices)

