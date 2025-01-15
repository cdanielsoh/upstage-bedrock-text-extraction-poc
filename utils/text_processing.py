from pathlib import Path
import json
import re


def aggregate_text_per_image(directory):
    """
    OCR/Docparse is processed after the source image is split.
    This function aggregates multiple JSON documents that were created after the source image was split back to one piece.

    :param directory:
    """
    text_data = {}
    file_locations = {}  # Store the parent directory of each prefix

    for file_path in Path(directory).rglob('*.json'):
        file_name = file_path.name

        if file_name.endswith("_agg.json"):
            continue

        if "_cropped_" in file_name:
            prefix = file_name.split("_cropped_")[0]
        else:
            prefix = file_name.replace(".json", "")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            text = data.get("text", "")

        if prefix not in text_data:
            text_data[prefix] = []
            file_locations[prefix] = file_path.parent  # Store the parent directory

        text_data[prefix].append((file_name, text))

    for prefix, texts in text_data.items():
        texts.sort(key=lambda x: x[0])

        combined_text = " ".join(text for _, text in texts)
        agg_data = {"text": combined_text}

        # Use the stored parent directory to save in the same subdirectory
        output_path = file_locations[prefix] / f"{prefix}_agg.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(agg_data, f, ensure_ascii=False, indent=4)


def aggregate_json_files(source_folder: str | Path, destination_folder: str | Path):
    """
    Aggregates JSON documents that belong to the same item_cd.
    Disregards JSON documents that do not contain int or float to minimize input tokens.
    Creates a new directory destination_folder, and stores aggregated JSON in that directory.

    <item_cd>_agg.json:
    {
        <image_file_name1>: <text>.
        <image_file_name2>: <text>.
    }

    :param source_folder:
    :param destination_folder:
    """
    # Convert string paths to Path objects if necessary
    source_path = Path(source_folder)
    dest_path = Path(destination_folder)

    # Create destination folder if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)

    # Iterate through subfolders in the source folder
    for subfolder in source_path.iterdir():
        if subfolder.is_dir() and subfolder.name.startswith("item_cd="):
            item_cd = subfolder.name.split("=")[1]
            aggregated_data = {}

            # Find all _agg.json files in the subfolder
            sorted_jsons = sorted(subfolder.glob("*_agg.json"), key=lambda x: x.name)
            for json_file in sorted_jsons:
                # Read the JSON file and extract the "text" field
                data = json.loads(json_file.read_text())
                if re.search(r'\d+', data["text"]):
                    img_filename = json_file.name[:-9] + ".jpg"
                    aggregated_data[img_filename] = data["text"]

            # Write the aggregated data to a new JSON file in the destination folder
            output_file = dest_path / f"{item_cd}_agg.json"
            output_file.write_text(json.dumps(aggregated_data, ensure_ascii=False, indent=4))
