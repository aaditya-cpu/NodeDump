# # import subprocess
# # import re
# # import asyncio
# # import xml.etree.ElementTree as ET
# # import json

# # # Function to remove HTML tags
# # def remove_html_tags(text):
# #     return re.sub('<.*?>', '', text)

# # async def main():
# #     # Execute Pandoc command
# #     command = "pandoc -s yellow.docx -o output.html"
# #     try:
# #         process = await asyncio.create_subprocess_shell(
# #             command,
# #             stdout=asyncio.subprocess.PIPE,
# #             stderr=asyncio.subprocess.PIPE,
# #         )

# #         stdout, stderr = await process.communicate()

# #         print(f"stdout: {stdout.decode()}")
# #         if stderr:
# #             print(f"stderr: {stderr.decode()}")

# #     except Exception as e:
# #         print(f"Error executing Pandoc command: {e}")
# #         return

# #     # Read the HTML output
# #     try:
# #         with open("output.html", "r", encoding="utf-8") as f:
# #             data = f.read()

# #         # Remove HTML tags
# #         clean_data = remove_html_tags(data)

# #         # Convert to XML by wrapping in a root element
# #         root = ET.Element("root")
# #         content = ET.SubElement(root, "content")
# #         content.text = clean_data

# #         tree = ET.ElementTree(root)

# #         # Write back to output_modified.xml
# #         tree.write("output_modified.xml")

# #         # Create JSON content
# #         json_content = {"content": clean_data}

# #         # Write JSON to output.json
# #         with open("output.json", "w", encoding="utf-8") as json_file:
# #             json.dump(json_content, json_file, ensure_ascii=False, indent=4)

# #     except Exception as e:
# #         print(f"Error reading or writing file: {e}")

# # # Asynchronous main function call
# # if __name__ == "__main__":
# #     asyncio.run(main())
     
# import subprocess
# import re
# import asyncio
# import xml.etree.ElementTree as ET
# import json

# def remove_html_tags(text):
#     return re.sub('<.*?>', '', text)

# def create_question_xml(raw_data):
#     questions_elem = ET.Element("questions")
#     try:
#         for i, question_chunk in enumerate(re.split(r'\n(?=\d+\.)', raw_data)):
#             question_elem = ET.SubElement(questions_elem, "question", id=str(i+1))
#             mathml_blocks = re.findall(r'\$\$(.*?)\$\$', question_chunk, re.DOTALL)
#             lines = question_chunk.strip().split('\n')
            
#             question_text = lines[0][lines[0].find('.')+1:].strip()
#             ET.SubElement(question_elem, "text").text = question_text
            
#             options_elem = ET.SubElement(question_elem, "options")
#             option_idx = 0
#             for line in lines[1:]:
#                 option_match = re.match(r'(a|b|c|d)\)', line)
#                 if option_match:
#                     option_elem = ET.SubElement(options_elem, "option", value=option_match.group(1))
                    
#                     if mathml_blocks and option_idx < len(mathml_blocks):
#                         option_elem.text = mathml_blocks[option_idx]
#                         option_idx += 1
#                     else:
#                         print(f"Warning: No MathML block available for option index {option_idx}")
#     except Exception as e:
#         print(f"Error while processing XML: {e}")
    
#     return questions_elem

# # def create_question_xml(raw_data):
# #     questions_elem = ET.Element("questions")
# #     for i, question_chunk in enumerate(re.split(r'\n(?=\d+\.)', raw_data)):
# #         question_elem = ET.SubElement(questions_elem, "question", id=str(i+1))
# #         mathml_blocks = re.findall(r'\$\$(.*?)\$\$', question_chunk, re.DOTALL)
# #         lines = question_chunk.strip().split('\n')
# #         question_text = lines[0][lines[0].find('.')+1:].strip()
# #         ET.SubElement(question_elem, "text").text = question_text
# #         options_elem = ET.SubElement(question_elem, "options")
# #         option_idx = 0
# #         for line in lines[1:]:
# #             option_match = re.match(r'(a|b|c|d)\)', line)
# #             if option_match:
# #                 option_elem = ET.SubElement(options_elem, "option", value=option_match.group(1))
# #                 if mathml_blocks:
# #                     option_elem.text = mathml_blocks[option_idx]
# #                     option_idx += 1
# #     return questions_elem

# async def main():
#     # First part: Conversion from .docx to .html
#     command = "pandoc -s yellow.docx -o output.html"
#     try:
#         process = await asyncio.create_subprocess_shell(
#             command,
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE
#         )
#         stdout, stderr = await process.communicate()
#         print(f"stdout: {stdout.decode()}")
#         if stderr:
#             print(f"stderr: {stderr.decode()}")

#     except Exception as e:
#         print(f"Error executing Pandoc command: {e}")
#         return

#     # Second part: Cleaning the HTML output and saving it as XML
#     try:
#         with open("output.html", "r", encoding="utf-8") as f:
#             data = f.read()
#         clean_data = remove_html_tags(data)
#         root = ET.Element("root")
#         content = ET.SubElement(root, "content")
#         content.text = clean_data
#         tree = ET.ElementTree(root)
#         tree.write("output_modified.xml")

#         # Create JSON content
#         json_content = {"content": clean_data}
#         with open("output.json", "w", encoding="utf-8") as json_file:
#             json.dump(json_content, json_file, ensure_ascii=False, indent=4)

#     except Exception as e:
#         print(f"Error reading or writing file: {e}")
#         return

#     # Third part: Structuring the XML
#     try:
#         with open("output_modified.xml", "r", encoding="utf-8") as f:
#             raw_data = f.read()
#         raw_data = re.sub(r'(&#.*?;)', '', raw_data)
#         questions_elem = create_question_xml(raw_data)
#         root = ET.Element("root")
#         root.append(questions_elem)
#         tree = ET.ElementTree(root)
#         tree.write("structured_output.xml")

#     except Exception as e:
#         print(f"Error reading or writing file: {e}")

# # Run the main asynchronous function
# if __name__ == "__main__":
#     asyncio.run(main())
import subprocess
import re
import asyncio
import xml.etree.ElementTree as ET
import json

def remove_html_tags(text):
    return re.sub('<.*?>', '', text)

# New function to create question XML
def create_question_xml(raw_data):
    questions_elem = ET.Element("questions")
    try:
        for i, question_chunk in enumerate(re.split(r'\n(?=\d+\.)', raw_data)):
            question_elem = ET.SubElement(questions_elem, "question", id=str(i+1))
            lines = question_chunk.strip().split('\n')
            
            question_text = lines[0][lines[0].find('.')+1:].strip()
            ET.SubElement(question_elem, "text").text = question_text
            
            options_elem = ET.SubElement(question_elem, "options")
            
            for line in lines[1:]:
                option_match = re.match(r'(a|b|c|d)\)', line.strip())
                if option_match:
                    option_elem = ET.SubElement(options_elem, "option", value=option_match.group(1))
                    option_text = line[line.find(')')+1:].strip()
                    option_elem.text = option_text

    except Exception as e:
        print(f"Error while processing XML: {e}")
        return questions_elem

    return questions_elem

async def main():
    # First part: Conversion from .docx to .html
    command = "pandoc -s yellow.docx -o output.html"
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(f"stdout: {stdout.decode()}")
        if stderr:
            print(f"stderr: {stderr.decode()}")

    except Exception as e:
        print(f"Error executing Pandoc command: {e}")
        return

    # Second part: Cleaning the HTML output and saving it as XML
    try:
        with open("output.html", "r", encoding="utf-8") as f:
            data = f.read()
        clean_data = remove_html_tags(data)
        root = ET.Element("root")
        content = ET.SubElement(root, "content")
        content.text = clean_data
        tree = ET.ElementTree(root)
        tree.write("output_modified.xml")

        # Create JSON content
        json_content = {"content": clean_data}
        with open("output.json", "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error reading or writing file: {e}")
        return

    # Third part: Structuring the XML
    try:
        with open("output_modified.xml", "r", encoding="utf-8") as f:
            raw_data = f.read()
        raw_data = re.sub(r'(&#.*?;)', '', raw_data)
        questions_elem = create_question_xml(raw_data)
        root = ET.Element("root")
        root.append(questions_elem)
        tree = ET.ElementTree(root)
        tree.write("structured_output.xml")

    except Exception as e:
        print(f"Error reading or writing file: {e}")

# Run the main asynchronous function
if __name__ == "__main__":
    asyncio.run(main())
