# import asyncio
# import re
# from bs4 import BeautifulSoup
# from aiofiles import open as aio_open

# async def main():
#     try:
#         # Use output.html instead of output.txt for the proper HTML structure
#         process = await asyncio.create_subprocess_shell('pandoc -s --toc --section-divs red.docx -o output.html')
#         await process.communicate()
#         print("Pandoc command executed successfully.")
#         txt_process = await asyncio.create_subprocess_shell('pandoc -s red.docx -o output.txt')
#         await txt_process.communicate()

#         print("Pandoc commands executed successfully.")
#     except Exception as e:
#         print(f"Error executing Pandoc commands: {e}")
#         return
#     # except Exception as e:
#     #     print(f"Error executing Pandoc command: {e}")
#     #     return

#     async with aio_open('output.html', mode='r', encoding='utf-8') as f:
#         data = await f.read()

#     regex_list = [
#         re.compile(r"\$\$([\s\S]*?)\$\$"),
#         re.compile(r"\$([^\$]*)\$"),
#         re.compile(r"\\\[([\s\S]*?)\\\]"),
#         re.compile(r"\\\(([\s\S]*?)\\\)"),
#     ]

#     new_data = data
#     for regex in regex_list:
#         new_data = regex.sub(r"\\(\1\\)", new_data)

#     soup = BeautifulSoup(new_data, 'html.parser')

#     # Remove empty tags
#     for tag in soup.find_all(True):
#         if not tag.get_text(strip=True):
#             tag.extract()

#     # Check if head exists
#     if soup.head:
#         mathjax_script = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>'
#         soup.head.append(BeautifulSoup(mathjax_script, 'html.parser'))
#     else:
#         print("No <head> tag found. MathJax script was not appended.")

#     async with aio_open('output_modified.html', mode='w', encoding='utf-8') as f:
#         await f.write(str(soup))

#     print("File modification completed. Created output_modified.html")

# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
import re
from bs4 import BeautifulSoup
from aiofiles import open as aio_open

async def format_txt_to_csv(txt_path, csv_path):
    formatted_lines = []
    async with aio_open(txt_path, 'r', encoding='utf-8') as txt_file:
        lines = await txt_file.readlines()

    for line in lines:
        formatted_line = line.strip().split(" ")  # Assuming space-separated values
        formatted_lines.append(",".join(formatted_line))  # Convert to comma-separated

    async with aio_open(csv_path, 'w', encoding='utf-8') as csv_file:
        await csv_file.write("\n".join(formatted_lines))

async def main():
    try:
        process = await asyncio.create_subprocess_shell('pandoc -s --toc --section-divs red.docx -o output.html')
        await process.communicate()
        print("HTML Pandoc command executed successfully.")

        txt_process = await asyncio.create_subprocess_shell('pandoc -s red.docx -o output.txt')
        await txt_process.communicate()
        print("TXT Pandoc command executed successfully.")

    except Exception as e:
        print(f"Error executing Pandoc commands: {e}")
        return

    async with aio_open('output.html', mode='r', encoding='utf-8') as f:
        data = await f.read()

    regex_list = [
        re.compile(r"\$\$([\s\S]*?)\$\$"),
        re.compile(r"\$([^\$]*)\$"),
        re.compile(r"\\\[([\s\S]*?)\\\]"),
        re.compile(r"\\\(([\s\S]*?)\\\)"),
    ]

    new_data = data
    for regex in regex_list:
        new_data = regex.sub(r"\\(\1\\)", new_data)

    soup = BeautifulSoup(new_data, 'html.parser')

    for tag in soup.find_all(True):
        if not tag.get_text(strip=True):
            tag.extract()

    if soup.head:
        mathjax_script = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>'
        soup.head.append(BeautifulSoup(mathjax_script, 'html.parser'))
    else:
        print("No <head> tag found. MathJax script was not appended.")

    async with aio_open('output_modified.html', mode='w', encoding='utf-8') as f:
        await f.write(str(soup))

    print("File modification completed. Created output_modified.html")

    # Call the function to format the output.txt to CSV format
    await format_txt_to_csv('output.txt', 'output_formatted.csv')

if __name__ == "__main__":
    asyncio.run(main())
