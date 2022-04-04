#!/usr/bin/env python3

import os
import json
import nibabel
import numpy as np
import io

with open('config.json', encoding='utf8') as config_json:
    config = json.load(config_json)

img = nibabel.load(config["t1"])

results = {}

results["headers"] = {}
for key in img.header:
    value = img.header[key]
    results['headers'][key] = value
results['headers']['base_affine'] = img.header.get_base_affine().tolist()

data = img.get_fdata()
results["voxel_histogram"] = np.histogram(data, bins=100, range=(0, 1500))

if not os.path.exists("output"):
    os.makedirs("output")

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)

with open("output/stats.json", "w") as outfile:
    json.dump(results, outfile, cls=NumpyEncoder)

print("done");
