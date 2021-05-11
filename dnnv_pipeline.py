import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as rt
import os
import subprocess
import sys

# Execute DNNV using the command line
def execute_dnnv_properties(dnn_onnx_path, verifier_name, properties_path, results_path, timeout=1800, degrees=15):
    if not os.path.exists(results_path + '/counter_examples'):
        os.makedirs(results_path + '/counter_examples')
    if not os.path.exists(results_path + '/dnnv_output'):
        os.makedirs(results_path + '/dnnv_output')
    for filename in sorted(os.listdir(properties_path)):
        if filename.endswith('.py'):
            property_name = filename.split('.')[0]
            print("VERIFYING PROPERTY: " + str(filename))
            with open(results_path + '/dnnv_output/results_' + property_name + '.txt', 'w') as f:
                subprocess.run(
                    ['timeout', "--signal=SIGINT", timeout,
                    'dnnv', properties_path + '/' + filename,
                    '--network', 'N', dnn_onnx_path, 
                    '--' + verifier_name.lower(),
                    '--save-violation', results_path + '/counter_examples/ce_' + property_name,
                    '--prop.gamma', degrees],
                stdout=f, stderr=f, text=True)


# Generate JSON with important data from Result
def get_data_from_result_file(file_path, timeout):
    result_file = open(file_path, "r")

    result = {}
    result['status'] = None
    result['time'] = None

    for l in result_file:
        if("result: " in l):
            result['status'] = l.split('result: ')[1].split('\n')[0]
        
        if("time: " in l):
            result['time'] = l.split("time: ")[1].split('\n')[0]

        if("KeyboardInterrupt" in l):
            result['status'] = "timeout"
            result['time'] = timeout

        if("OSError: [Errno 28] No space left on device" in l):
            result['status'] = "OSError: [Errno 28] No space left on device"
            result['time'] = timeout
            
    result_file.close()
    return result


def create_digit_image(imgNumber, results_path, filename, properties_path, dnn_path, degrees):
    if os.path.exists(results_path + '/counter_examples/ce_property' + str(imgNumber) + '.npy'):

        ### Load ONNX model
        sess = rt.InferenceSession(dnn_path)
        input_name = sess.get_inputs()[0].name

        ### Predict steering angle of original img
        orig_img = np.load(properties_path + '/orig_img' + str(imgNumber) + '.npy') / 255
        pred_orig_img = sess.run(None, {input_name: orig_img.astype(np.float32).reshape(1,3,100,100)})[0]
        arrow_x1 = np.cos((90 * np.pi / 180) + pred_orig_img).item() * 30
        arrow_y1 = np.sin((90 * np.pi / 180) + pred_orig_img).item() * 30

        ### Predict steering angle of counter-example
        ce = np.load(results_path + '/counter_examples/ce_property' + str(imgNumber) + '.npy')
        pred_ce = sess.run(None, {input_name: ce.astype(np.float32)})[0]
        arrow_x2 = np.cos((90 * np.pi / 180) + pred_ce).item() * 30
        arrow_y2 = np.sin((90 * np.pi / 180) + pred_ce).item() * 30

        angle_diff = np.abs(pred_orig_img.item() - pred_ce.item()) * 180 / np.pi

        if angle_diff > float(degrees):
            image = np.moveaxis(ce[0], 0, -1)
            plt.clf()
            plt.axis('off');
            plt.imshow(image)
            plt.arrow(50, 99, arrow_x1, -arrow_y1, width = 0.5, head_width=3, head_length=3, color='black')
            plt.arrow(50, 99, arrow_x2, -arrow_y2, width = 0.5, head_width=3, head_length=3, color='red')
            plt.savefig(results_path + "/images/image"+str(imgNumber)+".png")
            return image
        else:
            result_file = open(results_path+"/dnnv_output/"+filename, "r")
            data = []

            for l in result_file:
                if("result: " in l):
                    data.append(l.split(': ')[0] + ": error (Counter-example not violating property)\n")
                else:
                    data.append(l)

            result_file.close()
            
            result_file = open(results_path+"/dnnv_output/"+filename, "w")
            result_file.writelines(data)
            result_file.close()

            return None
    else:
        return None


def generate_results(dnn_path, results_path, properties_path, degrees, timeout):

    if not os.path.exists(results_path + '/images'):
        os.makedirs(results_path + '/images')

    result_summary = open(results_path + "/result_summary.md", "w")
    for i, filename in enumerate(sorted(os.listdir(results_path + '/dnnv_output'))):

        decoded_digit = create_digit_image(i, results_path, filename, properties_path, dnn_path, degrees)

        result_summary.write("#Property " + str(i) + '\n')
        result_data = get_data_from_result_file(str(results_path+"/dnnv_output/"+filename), timeout)

        if(result_data['status'] != None):
            result_summary.write("##Status: " + result_data['status'] + '\n')
            result_summary.write("###Time: "+result_data['time']+'\n')

        

        if type(decoded_digit) == np.ndarray:
            result_summary.write("![](./images/image"+str(i)+".png)"+'\n')

    result_summary.close()


def main():
    if len(sys.argv) < 4:
        print("Need: Dnn path, properties path, results path, timeout, degrees and falsifier name")
        return

    dnn_path = sys.argv[1]
    properties_path = sys.argv[2]
    results_path = sys.argv[3]
    timeout = sys.argv[4]
    degrees = sys.argv[5]
    verifier_name = sys.argv[6]
    
    execute_dnnv_properties(dnn_path, verifier_name, properties_path, results_path, timeout, degrees)

    generate_results(dnn_path, results_path, properties_path, degrees, timeout)


if __name__ == '__main__':
    main()