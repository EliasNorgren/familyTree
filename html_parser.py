from bs4 import BeautifulSoup
import json
import re

with open("data/Bergman.htm", "r", encoding="windows-1252") as file:
    html = file.read()

print(html)
exit()

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
    hex_string = a_string.encode("utf-8").hex()

    print("-----", number, len(a_string), "-----")
    print(a_string)
    print(hex_string)

    if text:
        # Try to extract the name using regex
        match = re.search(r"\d+\s*<b>([^<]+)</b>", str(text))
        if match:
            name = match.group(1).strip()
            people.append({"number": number, "name": name})

# Print as JSON
print(json.dumps(people, ensure_ascii=False, indent=2))