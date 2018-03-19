import yaml

from collections import OrderedDict

def yaml_dump (filepath, data):
    #dumps data in a file
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)
    print("Data dumped in", filepath )

id = 1
bbox = {"x1": 41,
        "x2": 62,
        "y1": 187,
        "y2": 189,
            }
bboxes = [bbox]

data = {
    "path" : "cesta_k_souboru/video18.avi",
    "team" : ["Daniel Beran", "Hynek Marek"],
     "frames": {
#pro kazde id potrebuji list pro kazdy bbobx
#kazdy bbox je pak dict s dvojicemi souradnic
        id: bboxes
    }
}
filepath = "test.yaml"
#print (yaml.dump(data, default_flow_style=False))

yaml_dump(filepath, data)