// const mammoth = require("mammoth");
// const fs = require("fs");

// const sourcePath = "wewf.rtf"; // Replace with the path to your docx file
// const destinationPath = "output.html"; // Replace with the path where you'd like to save the HTML output

// mammoth.convertToHtml({path: sourcePath})
//     .then(displayResult)
//     .catch(handleError);

// function displayResult(result) {
//     const html = result.value; // The generated HTML
//     const messages = result.messages; // Any messages, such as warnings during conversion

//     fs.writeFile(destinationPath, html, function(err) {
//         if (err) {
//             return console.log(err);
//         }
//         console.log("The file was saved!");
//     });

//     console.log("Messages: ", messages);
// }

// function handleError(err) {
//     console.log(err);
// }
// const { exec } = require('child_process');

// // Replace 'input.docx' and 'output.html' with your actual file paths
// const command = 'pandoc -s red.docx -o output.html';

// exec(command, (error, stdout, stderr) => {
//     if (error) {
//         console.error(`Error executing command: ${error}`);
//         return;
//     }
//     console.log(`stdout: ${stdout}`);
//     console.log(`stderr: ${stderr}`);
// });
// Import required modules
// const util = require('util');
// const fs = require('fs');
// const exec = util.promisify(require('child_process').exec);
// const readFile = util.promisify(fs.readFile);
// const writeFile = util.promisify(fs.writeFile);

// // Main function to execute all operations
// async function main() {
//   // Execute Pandoc command
//   const command = 'pandoc -s red.docx -o output.html';
//   try {
//     const { stdout, stderr } = await exec(command);
//     console.log(`stdout: ${stdout}`);
//     console.log(`stderr: ${stderr}`);
//   } catch (error) {
//     console.error(`Error executing Pandoc command: ${error}`);
//     return;
//   }

//   // Read the HTML file generated by Pandoc
//   try {
//     const data = await readFile('output.html', 'utf8');

//     // Regex to find LaTeX equations
//     const regex = /\$\$(.*?)\$\$/g;

//     // Replace LaTeX equations with MathJax compatible format
//     const newData = data.replace(regex, (match, p1) => `\\(${p1}\\)`);

//     // Insert MathJax script in HTML head
//     const mathJaxScript = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>';
//     const newDataWithMathJax = newData.replace('</head>', `${mathJaxScript}</head>`);

//     // Write the modified HTML to disk
//     await writeFile('output_modified.html', newDataWithMathJax, 'utf8');
//   } catch (err) {
//     console.error(`Error reading or writing file: ${err}`);
//   }
// }

// // Execute the main function
// main();
// Working code 

const util = require('util');
const fs = require('fs');
const exec = util.promisify(require('child_process').exec);
const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);

async function main() {
  const command = 'pandoc -s red.docx -o output.html';
  try {
    const { stdout, stderr } = await exec(command);
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
  } catch (error) {
    console.error(`Error executing Pandoc command: ${error}`);
    return;
  }

  try {
    const data = await readFile('output.html', 'utf8');
    let regexArray = [
      /\$\$([\s\S]*?)\$\$/g, // for $$...$$
      /\$([^\$]*)\$/g, // for $...$
      /\\\[([\s\S]*?)\\\]/g, // for \[...\]
      /\\\(([\s\S]*?)\\\)/g, // for \(...\)
    ];

    let newData = data;

    for (const regex of regexArray) {
      newData = newData.replace(regex, (match, p1) => `\\(${p1}\\)`);
    }

    const mathJaxScript = '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>';
    const newDataWithMathJax = newData.replace('</head>', `${mathJaxScript}</head>`);
    await writeFile('output_modified.html', newDataWithMathJax, 'utf8');
  } catch (err) {
    console.error(`Error reading or writing file: ${err}`);
  }
}

main();
