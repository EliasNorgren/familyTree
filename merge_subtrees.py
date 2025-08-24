import os
import json

result = {}

for file in os.listdir("corrected_output"):
    print("Processing", file)
    if not file.endswith(".json"):
        continue
    
    with open(f"corrected_output/{file}", "r", encoding="utf-8") as f:
        data = json.load(f)
    for person in data:
        number = int(person["number"])
        if number not in result:
            result[number] = person
        else:
            existing = result[number]
            # print(f"Conflict for number {number}:")
            # print(f"1. Existing: {existing['name']} ({existing['relationship']}) {existing['suffix']}")
            # print(f"2. New:      {person['name']} ({person['relationship']}) {person['suffix']}")
            # choice = input("Choose (1/2) or skip (s): ").strip().lower()
            if len(existing["suffix"]) > len(person["suffix"]):
                choice = '1'

            if choice == '1':
                continue
            elif choice == '2':
                result[number] = person
            else:
                print("Skipping...")
                continue

print(f"Merged total of {len(result)} unique individuals.")
with open("merged_output/merged.json", "w", encoding="utf-8") as f:
    json.dump(list(result.values()), f, ensure_ascii=False, indent=2)