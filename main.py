# import subprocess
# import re
# import asyncio
# from aiofiles import open as aio_open
# from bs4 import BeautifulSoup

# async def main():
#     # 1. Run pandoc command to convert docx to html
#     command = 'pandoc -s yellow.docx -o output.html'
#     try:
#         process = await asyncio.create_subprocess_shell(command)
#         await process.communicate()
#         print("Pandoc command executed successfully.")
#     except Exception as e:
#         print(f"Error executing Pandoc command: {e}")
#         return
    
#     # 2. Read the HTML file and apply transformations
#     try:
#         async with aio_open('output.html', mode='r', encoding='utf-8') as f:
#             data = await f.read()
        
#         # Replace MathJax-related strings
#         regex_array = [
#             re.compile(r'\$\$([\s\S]*?)\$\$'),  # for $$...$$
#             re.compile(r'\$([^\$]*)\$'),  # for $...$
#             re.compile(r'\\\[([\s\S]*?)\\\]'),  # for \[...\]
#             re.compile(r'\\\(([\s\S]*?)\\\)')  # for \(...\)
#         ]
        
#         new_data = data
#         for regex in regex_array:
#             new_data = regex.sub(r'\\(\1\\)', new_data)

#         # Insert MathJax script
#         mathjax_script = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>'
#         new_data_with_mathjax = re.sub('</head>', f'{mathjax_script}</head>', new_data)

#         async with aio_open('output_modified.html', mode='w', encoding='utf-8') as f:
#             await f.write(new_data_with_mathjax)
        
#         print("File modification completed.")
        
#     except Exception as e:
#         print(f"Error reading or writing file: {e}")
#         return

#     # 3. Convert modified HTML to structured XML
#     try:
#         async with aio_open('output_modified.html', 'r', encoding='utf-8') as f:
#             data = await f.read()
#         soup = BeautifulSoup(data, 'lxml')
        
#         xml_structure = '<?xml version="1.0" encoding="UTF-8"?>\n<questions>\n'
#         questions = soup.find_all('tr')
#         question_no = 0
        
#         for question in questions:
#             tds = question.find_all(['th', 'td'])
#             if len(tds) == 0:
#                 continue
            
#             if tds[0].text.strip().isnumeric():
#                 question_no = tds[0].text.strip()
#                 xml_structure += f'  <question id="{question_no}">\n'
#                 xml_structure += f'    <content>{tds[1].text.strip()}</content>\n'
#                 continue
            
#             if not question_no:
#                 continue
            
#             option_tag = tds[1].text.strip()
#             option_content = tds[2].text.strip()
#             xml_structure += f'    <option tag="{option_tag}">{option_content}</option>\n'
            
#             if option_tag.lower() == 'd':
#                 xml_structure += '  </question>\n'
#                 question_no = 0
        
#         xml_structure += '</questions>'
        
#         async with aio_open('questions.xml', 'w', encoding='utf-8') as f:
#             await f.write(xml_structure)
        
#         print("XML file created successfully.")
        
#     except Exception as e:
#         print(f"Error reading or writing file: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())
import subprocess
import re
import asyncio
from bs4 import BeautifulSoup
from aiofiles import open as aio_open

async def main():
    # Run pandoc command to convert docx to html
    command = 'pandoc -s red.docx -o output.html'
    try:
        process = await asyncio.create_subprocess_shell(command)
        await process.communicate()
        print("Pandoc command executed successfully.")
    except Exception as e:
        print(f"Error executing Pandoc command: {e}")
        return
    
    # Read the HTML file
    try:
        async with aio_open('output.html', mode='r', encoding='utf-8') as f:
            data = await f.read()

        # ... [Previous code for handling MathJax here] ...

        # Parse HTML content
        soup = BeautifulSoup(data, 'lxml')
        xml_structure = '<?xml version="1.0" encoding="UTF-8"?>\n<questions>\n'
        
        questions = soup.find_all('tr', class_='odd')
        options = soup.find_all('tr', class_='even')
        
        for q, o in zip(questions, options):
            question_number = q.find('td').text.strip()
            question_content = q.find_all('td')[1].text.strip()
            
            xml_structure += f'  <question id="{question_number}">\n'
            xml_structure += f'    <content>{question_content}</content>\n'
            
            option_tags = o.find_all('td')[1::2]
            option_contents = o.find_all('td')[2::2]
            
            for tag, content in zip(option_tags, option_contents):
                option_tag = tag.text.strip()
                option_content = content.text.strip()
                
                xml_structure += f'    <option tag="{option_tag}">{option_content}</option>\n'
            
            xml_structure += '  </question>\n'
        
        xml_structure += '</questions>'
        
        # Write to XML file
        async with aio_open('questions.xml', 'w', encoding='utf-8') as f:
            await f.write(xml_structure)
        print("XML file created successfully.")
        
    except Exception as e:
        print(f"Error reading or writing file: {e}")

if __name__ == "__main__":
    asyncio.run(main())
