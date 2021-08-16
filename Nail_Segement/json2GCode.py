# Develop by Bolin 
# Date: Aug 16th, 2021
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

def transform(polygon):
    content = ''
    for key, value in polygon.items():
        content += 'G01 X'
        content += str(value)
        content += ' Y' + str(value) + '\n'
    return content

def write_file(polygon, output_file):
    content = transform(polygon)
    with open(output_file, 'w') as o:
        o.write(content)
    o.close()
        
def run(args):
    output_dir = create_output_path()
    for label_file in glob.glob(os.path.join(args.input_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            output_file = create_output_file(output_dir, label_file)
            
            data = json.load(f)
            if data['outputs']:
                for output in data['outputs']['object']:
                    if 'polygon' in output.keys():
                        polygon = output['polygon']
                        name = output['name']
                        write_file(polygon, output_file)
                
if __name__ == '__main__':
    args = parse_args()
    run(args)