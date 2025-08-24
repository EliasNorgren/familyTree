from bs4 import BeautifulSoup
import json
import re


# print(html)
# exit()
def parse_html(html_file):
    with open(f"data/{html_file}", "r", encoding="windows-1252") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")

    people = []

    # Find all <a name="..."> tags that are followed by a number and a name
    for a in soup.find_all("a", attrs={"name": re.compile(r"\d+")}):
        
        # The ahnentafel number is in the name attribute
        number = a["name"]
        # The next sibling should contain the person info
        text = a.test
        a_string = a.decode_contents()
        
        if len(a_string) == 1 or "Generation" in a_string:
            continue


        if "<font" in a_string:
            a_string = re.sub(r"<font[^>]*>", "", a_string)
            a_string = a_string.replace("</font>", "")

        if "<br>" in a_string:
            a_string = a_string.replace("<br>", " ")

        if "</br>" in a_string:
            a_string = a_string.replace("</br>", " ")

        if "<br/>" in a_string:
            a_string = a_string.replace("<br/>", " ")

        if "[" in a_string:
            a_string = a_string.replace("[", "")

        a_string = a_string.replace("\n", " ").replace("\r", " ").replace("  ", " ").strip()
        # hex_string = a_string.encode("utf-8").hex()

        print("-----", number, len(a_string), "-----")
        print(a_string)
        # print(hex_string)
        relationship = a_string.split(" ")[0].strip()
        name_start = a_string.index("<b>")
        name_end = a_string.index("</b>")
        name = a_string[name_start + 3:name_end].strip()
        suffix_string = a_string[name_end + 4 :].strip()
        print("Name", name)
        print("Relationship:", relationship)
        print("Suffix:", suffix_string)
        entry = {
            "number": number,
            "name": name,
            "relationship": relationship,
            "suffix": suffix_string,
        }
        people.append(entry)

    # Print as JSON
    print(json.dumps(people, ensure_ascii=False, indent=2))

    with open(f"output/{html_file}.json", "w", encoding="utf-8") as f:
        json.dump(people, f, ensure_ascii=False, indent=2)


# All files in data/
import os
for filename in os.listdir("data"):
    if filename.endswith(".htm"):
        print("Processing", filename)
        parse_html(filename)

