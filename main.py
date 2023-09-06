import subprocess
import re
import asyncio
import xml.etree.ElementTree as ET
import json

# Function to remove HTML tags
def remove_html_tags(text):
    return re.sub('<.*?>', '', text)

async def main():
    # Execute Pandoc command
    command = "pandoc -s yellow.docx -o output.html"
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        print(f"stdout: {stdout.decode()}")
        if stderr:
            print(f"stderr: {stderr.decode()}")

    except Exception as e:
        print(f"Error executing Pandoc command: {e}")
        return

    # Read the HTML output
    try:
        with open("output.html", "r", encoding="utf-8") as f:
            data = f.read()

        # Remove HTML tags
        clean_data = remove_html_tags(data)

        # Convert to XML by wrapping in a root element
        root = ET.Element("root")
        content = ET.SubElement(root, "content")
        content.text = clean_data

        tree = ET.ElementTree(root)

        # Write back to output_modified.xml
        tree.write("output_modified.xml")

        # Create JSON content
        json_content = {"content": clean_data}

        # Write JSON to output.json
        with open("output.json", "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error reading or writing file: {e}")

# Asynchronous main function call
if __name__ == "__main__":
    asyncio.run(main())
     