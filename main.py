import asyncio
import re
from bs4 import BeautifulSoup
from aiofiles import open as aio_open

async def main():
    # 1. Run pandoc command to convert docx to html
    try:
        process = await asyncio.create_subprocess_shell('pandoc -s red.docx -o output.html')
        await process.communicate()
        print("Pandoc command executed successfully.")
    except Exception as e:
        print(f"Error executing Pandoc command: {e}")
        return

    # 2. Read the HTML file and apply transformations
    async with aio_open('output.html', mode='r', encoding='utf-8') as f:
        data = await f.read()

    soup = BeautifulSoup(data, 'html.parser')

    # Remove empty or whitespace-only tr and td tags
    for tag in soup.find_all(['tr', 'td']):
        if not tag.get_text(strip=True):
            tag.extract()

    # Add MathJax for rendering LaTeX
    mathjax_script = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>'
    soup.head.append(BeautifulSoup(mathjax_script, 'html.parser'))

    async with aio_open('output_modified.html', mode='w', encoding='utf-8') as f:
        await f.write(str(soup))

    print("File modification completed.")

    # 3. Convert modified HTML to structured XML
    async with aio_open('output_modified.html', mode='r', encoding='utf-8') as f:
        data = await f.read()

    soup = BeautifulSoup(data, 'lxml')
    xml_structure = '<?xml version="1.0" encoding="UTF-8"?>\n<questions>\n'
    
    questions = soup.find_all('tr', class_='odd')
    options = soup.find_all('tr', class_='even')

    for q, o in zip(questions, options):
        question_cells = q.find_all('td')
        option_cells = o.find_all('td')

        if len(question_cells) < 2 or len(option_cells) < 2:
            continue

        question_number = question_cells[0].text.strip()
        question_content = question_cells[1].text.strip()

        xml_structure += f'  <question id="{question_number}">\n'
        xml_structure += f'    <content>{question_content}</content>\n'
        
        option_tags = option_cells[::2]
        option_contents = option_cells[1::2]

        for tag, content in zip(option_tags, option_contents):
            option_tag = tag.text.strip()
            option_content = content.text.strip()
            
            xml_structure += f'    <option tag="{option_tag}">{option_content}</option>\n'
        
        xml_structure += '  </question>\n'
    
    xml_structure += '</questions>'
    
    async with aio_open('questions.xml', 'w', encoding='utf-8') as f:
        await f.write(xml_structure)

    print("XML file created successfully.")

if __name__ == "__main__":
    asyncio.run(main())
