from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image("generated_properties/dave_small_orig_img0.npy") / 255.0
input_layer = 0
output_layer = -2

lb = np.load("generated_properties/dave_small_lb0.npy") / 255.0
ub = np.load("generated_properties/dave_small_ub0.npy") / 255.0

gamma = Parameter("gamma", type=float, default=2.0) * np.pi / 180
output = N[input_layer:](x)
gamma_lb = np.tan(max(-np.pi / 2, (output - gamma) / 2))
gamma_ub = np.tan(min(np.pi / 2, (output + gamma) / 2))
Forall(
    x_,
    Implies(
        (0 <= x_ <= 1) & (lb < x_ < ub),
        (gamma_lb < N[input_layer:output_layer](x_) < gamma_ub),
    ),
)