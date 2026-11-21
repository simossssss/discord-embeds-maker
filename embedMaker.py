from datetime import datetime, timezone
from pathlib import Path
if not Path("./countCurrent").is_file():
    with open("countCurrent","w") as f:
        f.write("0")

def multInput(x: str) -> str:
    print(x, "\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":

    #<---- User prefrences ---->
    print("Discord Embed Creator")
    print("Choose what you want for your embed")

    hasTitle = input("Title (Y/N): ").strip().upper()
    while hasTitle not in ("Y", "N"):
        hasTitle = input("*specify again. Title (Y/N): ").strip().upper()

    hasDescription = input("Description (Y/N): ").strip().upper()
    while hasDescription not in ("Y", "N"):
        hasDescription = input("*Specify again. Description (Y/N): ").strip().upper()

    hasThumbnail = input("Thumbnail (Y/N): ").strip().upper()
    while hasThumbnail not in ("Y", "N"):
        hasThumbnail = input("*specify again. Thumbnail (Y/N): ").strip().upper()

    hasColor = input("Color (Y/N): ").strip().upper()
    while hasColor not in ("Y", "N"):
        hasColor = input("*specify again. Color (Y/N): ").strip().upper()

    hasFields = input("Fields (Y/N): ").strip().upper()
    while hasFields not in ("Y", "N"):
        hasFields = input("*specify again. Fields (Y/N): ").strip().upper()

    hasImage = input("Image (Y/N): ").strip().upper()
    while hasImage not in ("Y", "N"):
        hasImage = input("*specify again. Image (Y/N): ").strip().upper()

    hasFooter = input("Footer (Y/N): ").strip().upper()
    while hasFooter not in ("Y", "N"):
        hasFooter = input("*specify again. Footer (Y/N): ").strip().upper()

    hasAuthor = input("Author (Y/N): ").strip().upper()
    while hasAuthor not in ("Y", "N"):
        hasAuthor = input("*specify again. Author (Y/N): ").strip().upper()

    hasTimestamp = input("Timestamp (Y/N): ").strip().upper()
    while hasTimestamp not in ("Y", "N"):
        hasTimestamp = input("*specify again. Timestamp (Y/N): ").strip().upper()

    # <---- Announcement Save ---->
    count_path = Path("count")
    if count_path.exists():
        count = int(count_path.read_text(encoding="utf-8").strip()) + 1
    else:
        count = 1

    save = Path("ann") / f"{count}-announcement"
    save.mkdir(parents=True, exist_ok=True)

    if hasTitle == "Y":
        title = input("Type the title: ").strip()
        with open(save / "Title", "w", encoding="utf-8") as f:
            f.write(title)

    if hasDescription == "Y":
        description = multInput("Type the description: ")
        with open(save / "Description", "w", encoding="utf-8") as f:
            f.write(description)

    if hasThumbnail == "Y":
        thumbnail = input("Thumbnail url: ").strip().strip("<>\"'")
        with open(save / "Thumbnail", "w", encoding="utf-8") as f:
            f.write(thumbnail)

    if hasColor == "Y":
        color = input("Type the color code (6-digit): ").strip().lstrip("#")
        with open(save / "Color", "w", encoding="utf-8") as f:
            f.write(color)

    if hasFields == "Y":
        try:
            fieldcount = int(input("Field number: ").strip())
        except ValueError:
            fieldcount = 0
        with open(save / "FieldCount", "w") as f:
            f.write(str(fieldcount))
        fields = []
        for i in range(max(0, min(fieldcount, 25))):
            fieldName = input("Field name: ").strip()
            while not fieldName:
                fieldName = input("*field name is required: ").strip()

            fieldBody = multInput("Field contents: ")
            while not fieldBody:
                fieldBody = multInput("*field contents are required: ")

            inline = input("Inline (Y/N): ").strip().upper() == "Y"
            fields.append([fieldName, fieldBody, inline])

            with open(save / f"{i}-FieldName", "w", encoding="utf-8") as f:
                f.write(fieldName)
            with open(save / f"{i}-FieldBody", "w", encoding="utf-8") as f:
                f.write(fieldBody)
            with open(save / f"{i}-FieldInline", "w", encoding="utf-8") as f:
                f.write(str(inline))

    if hasImage == "Y":
        image = input("Image url: ").strip().strip("<>\"'")
        with open(save / "Image", "w", encoding="utf-8") as f:
            f.write(image)

    if hasFooter == "Y":
        footer = input("Footer context: ").strip()
        with open(save / "Footer", "w", encoding="utf-8") as f:
            f.write(footer)

    if hasAuthor == "Y":
        author = input("Author: ").strip()
        with open(save / "Author", "w", encoding="utf-8") as f:
            f.write(author)

    if hasTimestamp == "Y":
        timestamp = datetime.now(timezone.utc).isoformat()
        with open(save / "Timestamp", "w", encoding="utf-8") as f:
            f.write(timestamp)

    with open(count_path, "w", encoding="utf-8") as f:
        f.write(str(count))