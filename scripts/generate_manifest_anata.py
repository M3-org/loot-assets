import os
import json

def generate_manifest(directory_path):
    manifest_template = {
        "assetsLocation": "./loot-assets/anata/male/",
        "format": "vrm",
        "traitsDirectory": "",
        "thumbnailsDirectory": "./loot-assets/loot/thumbnails/",
        "exportScale": 1,
        "animationPath": get_animation_paths(),
        "traitIconsDirectorySvg": "./loot-assets/loot/icons/",
        "defaultCullingLayer": -1,
        "defaultCullingDistance": [0.1, 0.01],
        "initialTraits": ["Body", "Head", "Hands", "Shoes", "Chest", "Waist", "Neck"], 
        "offset": [0.0, 0.48, 0.0],
        "traits": generate_traits(directory_path),
        "textureCollections": [],
        "colorCollections": []
    }

    return json.dumps(manifest_template, indent=2)

def get_animation_paths():
    animation_directory = "./loot-assets/animations"
    animation_paths = [os.path.join(animation_directory, file) for file in os.listdir(animation_directory) if file.endswith(".fbx")]
    return sorted(animation_paths)


def generate_traits(directory_path):
    traits = []

    trait_culling_layers = {
        "Body": 0,
        "Head": -1,
        "Hands": -1,
        "Shoes": -1,
        "Chest": 0,
        "Neck": -1,
        "Weapon": -1,
        "Waist": -1
    }

    for trait_name, culling_layer in trait_culling_layers.items():
        trait = {
            "trait": trait_name,
            "name": trait_name.capitalize(),
            "icon": "",
            "type": "mesh",
            "iconGradient": "",
            "iconSvg": f"{trait_name.upper()}.svg",
            "cullingLayer": culling_layer,
            "cameraTarget": {"distance": 3.0, "height": 0.8},
            "cullingDistance": [0.1, 0.01],
            "collection": generate_collection(directory_path, trait_name)
        }

        traits.append(trait)

    return traits

def generate_collection(directory_path, trait_name):
    trait_directory_path = os.path.join(directory_path, trait_name)

    return [
        {
            "id": entry[:-4],
            "name": entry[:-4].replace("_", " "),
            "directory": f"{trait_name}/{entry}",
            "thumbnail": f"{trait_name}/{entry[:-4]}.png"
        }
        for entry in os.listdir(trait_directory_path)
        if entry.endswith(".vrm")
    ]

if __name__ == "__main__":
    directory_path = "./anata/male/"
    manifest_content = generate_manifest(directory_path)

    with open("./anata/male/manifest.json", "w") as manifest_file:
        manifest_file.write(manifest_content)

    print("Manifest file generated successfully.")
