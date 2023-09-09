import asyncio
from bs4 import BeautifulSoup, Tag
from aiofiles import open as aio_open
import re


async def run_pandoc():
    try:
        process = await asyncio.create_subprocess_shell('pandoc -s red.docx -o output.html')
        await process.communicate()
        print("Successfully converted red.docx to output.html")
        return True
    except Exception as e:
        print(f"Error running pandoc: {e}")
        return False


async def read_file(file_path):
    async with aio_open(file_path, mode='r', encoding='utf-8') as f:
        return await f.read()


async def write_file(file_path, data):
    async with aio_open(file_path, mode='w', encoding='utf-8') as f:
        await f.write(data)


def clean_html(soup):
    # Remove empty or whitespace-only tr and td tags
    for tag in soup.find_all(True):
        if not tag.contents:
            tag.extract()
        elif all(isinstance(c, Tag) and c.name == 'br' for c in tag.contents):
            tag.extract()
        elif not tag.get_text(strip=True):
            tag.extract()
    # Add MathJax for LaTeX rendering
    mathjax_script = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>'
    soup.head.append(BeautifulSoup(mathjax_script, 'html.parser'))
    return soup


def convert_to_xml(original_html):
    soup = BeautifulSoup(original_html, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        print(table.find("thead").text)
        trs = table.find("tbody").find_all("tr")
        optionStatus = False
        options2 = ""
        for index,tr in enumerate(trs):
            # print(tr.text)
            match = re.search(r'[\d.\.]{2,3}', tr.text)
            if match:
                questions = tr.text
                print(questions)
                optionStatus = True
                options2 = ""

            match = re.search(r'\b[a-d]\)', tr.text)
            options = ""
            # options2 = ""
            if match:
                for td in tr.find_all('td'):
                    options += td.text+"  "
                if optionStatus:
                    options2+=options+'  '
            if len(options2)>0:
                print(options2)


# def convert_to_xml(soup):
#     questions = soup.find_all('tr', class_='odd')
#     options = soup.find_all('tr', class_='even')
#     xml_structure = '<?xml version="1.0" encoding="UTF-8"?>\n<questions>\n'
#     for q, o in zip(questions, options):
#         question_cells = q.find_all('td')
#         option_cells = o.find_all('td')
#         if len(question_cells) < 2 or len(option_cells) < 2:
#             continue
#         question_number = question_cells[0].text.strip()
#         question_content = question_cells[1].text.strip()
#         xml_structure += f'  <question id="{question_number}">\n    <content>{question_content}</content>\n'
#         option_tags = option_cells[::2]
#         option_contents = option_cells[1::2]
#         for tag, content in zip(option_tags, option_contents):
#             option_tag = tag.text.strip()
#             option_content = content.text.strip()
#             xml_structure += f'    <option tag="{option_tag}">{option_content}</option>\n'
#         xml_structure += '  </question>\n'
#     xml_structure += '</questions>'
#     return xml_structure

async def main():
    # if not await run_pandoc():
    #     return
    # Load and clean the initial HTML
    original_html = await read_file('output.html')
    original_soup = BeautifulSoup(original_html, 'html.parser')
    convert_to_xml(original_html)
    cleaned_soup = clean_html(original_soup)
    await write_file('output_modified.html', str(cleaned_soup))
    print("Successfully modified output.html to output_modified.html")

    # Generate the XML structure
    modified_html = await read_file('output_modified.html')
    modified_soup = BeautifulSoup(modified_html, 'lxml')
    xml_data = convert_to_xml(modified_soup)
    await write_file('questions.xml', xml_data)
    print("Successfully generated questions.xml")

if __name__ == "__main__":
    asyncio.run(main())
