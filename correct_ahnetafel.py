import json
import os

def correct_ahnentafel(data, new_root, root_numberer):
    # Build a lookup by old number
    old_people = {int(person["number"]): person for person in data}
    # Prepare new list
    new_people = []
    # Map old number to new number
    def renumber(old_num, new_num):
        if old_num not in old_people:
            return
        person = old_people[old_num]
        print(f"Renumbering {old_num} to {new_num}: {person['name']}")
        # input()
        # Copy and update number
        new_entry = person.copy()
        new_entry["number"] = str(new_num)
        new_people.append(new_entry)
        # Recursively renumber ancestors
        renumber(old_num * 2, new_num * 2)
        renumber(old_num * 2 + 1, new_num * 2 + 1)
    # Start with new root
    renumber(root_numberer, new_root)
    return new_people

def correct_file(filename, new_root, root_number):
    with open(f"output/{filename}", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    corrected = correct_ahnentafel(json_data, new_root, root_number)
    outname = "corrected_output/" + filename
    with open(outname, "w", encoding="utf-8") as f:
        json.dump(corrected, f, ensure_ascii=False, indent=2)
    print(f"Saved corrected file as {outname}")

for file in os.listdir("output"):
    if file.endswith(".json") and file.startswith("Nr"):
        root_number = 1
        if "?" in file:
            root_number = 2
        if "?!" in file:
            root_number = 4
        new_root = int(file[2:file.index(".")])
        print(file, new_root)
        correct_file(file, new_root, root_number)

correct_file("Nr153.htm.json", 153, 1)