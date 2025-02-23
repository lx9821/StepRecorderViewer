# StepRecorderViewer

StepRecorderViewer is a tool designed to convert recorded steps from an .mht file into a detailed HTML report. This tool extracts general information, steps, and screenshots from the recording and presents them in a user-friendly HTML format. It also supports dark mode and allows users to view a video of the recorded steps.

Even though `psr.exe` will soon be discontinued by Microsoft, this project aims to help with the current output format `.mht` to produce a nicer output. Problems with the `.mht` files include lack of browser support and difficulty in extracting images.


![image](https://github.com/user-attachments/assets/80264ab0-17c9-49c4-a322-2c5f5bf4cf92)

![image](https://github.com/user-attachments/assets/301575d5-02c8-4777-b27b-ff0f05573a2e)

## Key Features

- 📋 **General Information Extraction**: Extracts and displays general information about the recording session, including recording start and end times, duration, recorded steps, missed steps, errors, and operating system details.
- 📝 **Step Details**: Provides detailed information for each recorded step, including timestamps, descriptions, and screenshots.
- 🖼️ **Screenshot Handling**: Extracts and displays screenshots for each step. If a screenshot is not available, a placeholder image is used.
- 🎥 **Video Generation**: Creates a video from the extracted screenshots, allowing users to view the recorded steps as a video.
- 🌙 **Dark Mode Support**: Includes a toggle switch to switch between light and dark modes for better readability.
- 🖨️ **Print-Friendly**: Provides a print-friendly version of the report, ensuring that all details are clearly visible when printed.
- 🔍 **Detail Level Selection**: Allows users to select the level of detail they want to see for each step (Basic, Medium, Full).

## How It Works

1. **Extract Information**: The tool reads the .mht file and extracts general information and step details using BeautifulSoup and regular expressions.
2. **Generate JSON**: The extracted information is written to a JSON file.
3. **Create HTML Report**: The tool uses a template HTML file to generate a detailed report, embedding the JSON data into the HTML.
4. **Generate Video (Optional)**: The tool can create a video from the extracted screenshots.
5. **Display Report**: The generated HTML report is opened in the default web browser.

## Usage

1. Place the .mht file in the same directory as the `StepConverter/convert.py` script.
2. Run the `StepConverter/convert.py` script:
    ```sh
    python StepConverter/convert.py
    ```
3. The tool will generate the HTML report and open it in the default web browser.

## File Structure

```
StepConverter/
├── convert.py
├── template.html
├── not_available.png
├── requirements.txt
└── README.md
```

## Dependencies

- BeautifulSoup
- xml.etree.ElementTree
- re
- json
- base64
- unicodedata
- textwrap
- os
- glob
- shutil
- subprocess
- datetime
- PIL (Pillow)
- moviepy
- hashlib

## Installation

Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.
