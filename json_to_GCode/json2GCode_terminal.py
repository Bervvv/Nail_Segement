# Develop by Bolin 
# Last Modified: Aug 18th, 2021
# Transform nail segement data from json to G Code

import argparse
import glob
import json
import os

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_dir', help='input json directory')
    return parser.parse_args()

def create_output_path():
    output_dir = os.path.join(args.input_dir, 'GCode')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print('Creating GCode directory:', output_dir)
    return output_dir
        
def create_output_file(output_dir, label_file):
    base = os.path.splitext(os.path.basename(label_file))[0]
    output_file = os.path.join(output_dir, base + '.nc')
    return output_file

def transform(width, output):
    content = 'G90\nG1Z3F200\nM03 S1000\n'
    # ***change factor below to adjust image total size***
    factor = 1
    # ***change factor above to adjust image total size***
    for key, value in output['polygon'].items():
        value *= factor
        if 'x' in key:
            if 'x1' == key: first = 'G01 X' + str(value)
            content += 'G01 X' + str(value)
        elif 'y' in key:
            value = adjust_width(width, value)
            if 'y1' == key: first += ' Y' + str(value) + '\n'
            content += ' Y' + str(value) + '\n'
    if first: content += first
    content += 'M05\nM02'
    return content

def adjust_width(width, y):
#     height = data['size']['height']
    # ***change factor below to aujst nail width***
    factor = 1
    # ***change factor above to aujst nail width***
    half_width = width // 2
    if y > half_width:
        y *= factor
    elif y < half_width:
        y = width - (width - y) * factor
    if y < 0: 
        raise ValueError("Factor is too large to show the full image, please check the function adjust_width") 
    return int(y)

def write_file(width, output, output_file):
    content = transform(width, output)
    with open(output_file, 'w') as o:
        o.write(content)
    o.close()     

def run(args):
    output_dir = create_output_path()
    for label_file in glob.glob(os.path.join(args.input_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file, encoding = 'utf8') as f:
            output_file = create_output_file(output_dir, label_file)
            data = json.load(f)
            if data['outputs']:
                width = data['size']['width']
                for output in data['outputs']['object']:
                    if 'polygon' in output.keys():
                        write_file(width, output, output_file)
                
if __name__ == '__main__':
    args = parse_args()
    run(args)