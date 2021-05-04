import inspect

def create_property(output_dir, prop_name):
    
    if output_dir[-1] != '/':
        output_dir = output_dir + '/'

    img = output_dir + 'orig_img' + prop_name + '.npy'
    lb = output_dir + 'lb' + prop_name + '.npy'
    ub = output_dir + 'ub' + prop_name + '.npy'

    property_file = open(output_dir + 'property' + prop_name + '.py', 'w')

    property_file.write(inspect.cleandoc(
    """
        from dnnv.properties import *
        import numpy as np

        N = Network("N")
        x = Image("{}") / 255.0
        input_layer = 0
        output_layer = -2

        lb = np.load("{}") / 255.0
        ub = np.load("{}") / 255.0

        gamma = Parameter("gamma", type=float, default=15.0) * np.pi / 180
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
    """.format(img, lb, ub)))

    property_file.close()


def main(args):
    # output_dir = 'generated_properties/'
    # prop_name = '0'
    create_property(args.output, args.name)


if __name__ == "__main__":
    main()