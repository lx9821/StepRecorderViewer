from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import json
import base64
import unicodedata
import textwrap
import os
import glob
import shutil
import subprocess
from datetime import datetime
from PIL import Image
from moviepy import ImageSequenceClip
import hashlib

def calculate_time_difference(start, end):
    # Convert strings to datetime objects
    start_time = datetime.strptime(start, "%d.%m.%Y %H:%M:%S")
    end_time = datetime.strptime(end, "%d.%m.%Y %H:%M:%S")
    
    # Calculate the difference
    delta = end_time - start_time
    
    # Extract days, hours, minutes, seconds
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Prepare result
    result = []
    if days > 0:
        result.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        result.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        result.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 or len(result) == 0:  # Ensure seconds is shown even if everything else is zero
        result.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    
    # Join and return
    return ", ".join(result)

def lookupSKU(sku, build):
    windows_skus = {
    0: {"edition": "Windows 10 Home", "description": "Standard edition for home users with basic features."},
    1: {"edition": "Windows 10 Pro", "description": "Pro version for small businesses and enthusiasts, includes advanced features like BitLocker."},
    2: {"edition": "Windows 10 Enterprise", "description": "Enterprise-focused edition with extra security and management features."},
    3: {"edition": "Windows 10 Education", "description": "Version tailored for educational institutions with extra management and security features."},
    4: {"edition": "Windows 10 Pro for Workstations", "description": "Optimized for high-performance workstations and server hardware."},
    5: {"edition": "Windows 10 Enterprise LTSB", "description": "Long-Term Servicing Branch with fewer updates, focused on stability."},
    6: {"edition": "Windows 10 Enterprise SAC", "description": "Semi-Annual Channel edition, designed for businesses that want regular updates."},
    7: {"edition": "Windows 10 IoT Core", "description": "Edition designed for small embedded systems like kiosks and ATMs."},
    8: {"edition": "Windows 10 IoT Enterprise", "description": "Advanced IoT edition with enterprise-level management and security."},
    9: {"edition": "Windows 10 S", "description": "Streamlined version that only allows apps from the Microsoft Store."},
    10: {"edition": "Windows 10 Team", "description": "Optimized for Surface Hub devices, focusing on collaborative work in meetings."},
    11: {"edition": "Windows 10 Education for Nonprofits", "description": "Education version tailored for nonprofit organizations, includes additional features."},
    12: {"edition": "Windows 10 Pro for Education", "description": "Pro version designed for schools and universities with management features."},
    13: {"edition": "Windows 10 Pro N", "description": "Pro version without media apps, available in regions like the EU."},
    14: {"edition": "Windows 10 Pro KN", "description": "Pro version without media apps, available in regions like South Korea."},
    15: {"edition": "Windows 10 Home N", "description": "Home version without media apps, available in regions like the EU."},
    16: {"edition": "Windows 10 Education N", "description": "Education version without media apps, available in regions like the EU."},
    17: {"edition": "Windows 10 Enterprise N", "description": "Enterprise version without media apps, available in regions like the EU."},
    18: {"edition": "Windows 10 Mobile", "description": "Version for smartphones and mobile devices (older versions, no longer supported)."},
    19: {"edition": "Windows 10 Mobile Enterprise", "description": "Mobile version for enterprise devices."},
    20: {"edition": "Windows 10 Cloud", "description": "Cloud-centric edition, now largely integrated into the Windows 10 S version."},
    21: {"edition": "Windows 10 Pro for Education N", "description": "Pro version for educational institutions without media apps."},
    22: {"edition": "Windows 10 Home China", "description": "China-specific version of Windows 10 Home with regional customizations."},
    23: {"edition": "Windows 10 Professional China", "description": "China-specific version of Windows 10 Pro with regional customizations."},
    24: {"edition": "Windows 10 Pro for Business", "description": "Professional version tailored for business environments with additional management tools."},
    25: {"edition": "Windows 10 Enterprise LTSC", "description": "Long-Term Servicing Channel version for specialized environments requiring stability."},
    48: {"edition": "Windows 10 Enterprise Multi-Session", "description": "Used in virtual environments (e.g., Windows Virtual Desktop) allowing multiple concurrent user sessions."},
    49: {"edition": "Windows 10 Pro Education", "description": "Pro version for educational institutions with education-specific features."},
    50: {"edition": "Windows 10 Pro Education Multi-Session", "description": "Pro Education with support for multiple simultaneous sessions in virtual environments."},
    51: {"edition": "Windows 10 Pro for ARM", "description": "Windows 10 Pro for ARM-based devices, designed for ARM processors."},
    52: {"edition": "Windows 10 Pro Education for ARM", "description": "ARM variant of Windows 10 Pro Education, tailored for educational institutions."},
    53: {"edition": "Windows 10 Enterprise for ARM", "description": "ARM variant of Windows 10 Enterprise, providing full enterprise management features."},
    54: {"edition": "Windows 10 Education N for ARM", "description": "ARM version of Windows 10 Education N (without media apps), for educational environments."},
    55: {"edition": "Windows 10 Enterprise N for ARM", "description": "ARM version of Windows 10 Enterprise N (without media apps), for enterprise customers."},
    56: {"edition": "Windows 10 Home for ARM", "description": "Home edition of Windows 10 for ARM-based devices, designed for ARM processors."},
    57: {"edition": "Windows 10 IoT Enterprise for ARM", "description": "ARM version of Windows 10 IoT Enterprise for embedded systems."},
    58: {"edition": "Windows 10 Enterprise LTSC (ARM)", "description": "Long-Term Servicing Channel edition of Windows 10 Enterprise for ARM-based devices."},
    59: {"edition": "Windows 10 Pro for Workstations (ARM)", "description": "Pro for Workstations tailored for ARM devices, optimized for high-performance computing."},
    60: {"edition": "Windows 10 IoT Core for ARM", "description": "Windows 10 IoT Core edition for ARM-based embedded devices."},
    61: {"edition": "Windows 10 Enterprise LTSC 2019", "description": "LTSC version of Windows 10 Enterprise from the 2019 release cycle."},
    62: {"edition": "Windows 10 Enterprise LTSC 2021", "description": "LTSC version of Windows 10 Enterprise from the 2021 release cycle."},
    63: {"edition": "Windows 10 Home Single Language", "description": "A specialized edition for certain markets with only one available language."},
    64: {"edition": "Windows 10 Pro Single Language", "description": "Pro version limited to a single language option, tailored for specific markets."},
    65: {"edition": "Windows 10 Home China", "description": "China-specific version of Windows 10 Home with local customizations."},
    66: {"edition": "Windows 10 Pro China", "description": "China-specific version of Windows 10 Pro with compliance features for the region."},
    67: {"edition": "Windows 10 Enterprise China", "description": "Enterprise version tailored for China with regional customizations."},
    68: {"edition": "Windows 10 Enterprise N China", "description": "Enterprise version without media apps for China."},
    69: {"edition": "Windows 10 Enterprise S", "description": "Enterprise version in S mode, restricting installations to Microsoft Store apps only."},
    70: {"edition": "Windows 10 Enterprise S N", "description": "Enterprise S version without media apps (e.g., Windows Media Player)."},
    71: {"edition": "Windows 10 Home Japan", "description": "Japan-specific version of Windows 10 Home with local language support."},
    72: {"edition": "Windows 10 Pro Japan", "description": "Japan-specific version of Windows 10 Pro, with local support and customizations."},
    73: {"edition": "Windows 10 Enterprise Japan", "description": "Japan-specific version of Windows 10 Enterprise with regional adjustments."}
    }
    sku_info = windows_skus.get(sku, {"edition": "Unknown", "description": "<i>No description available</i>"})

    if sku_info["edition"] == "Unknown":
        if build > 26000:
            sku_info["edition"] = "Windows 11"
            sku_info["description"] = "<i>No description available</i>"
        else:
            sku_info["edition"] = "Unknown Windows Edition"
            sku_info["description"] = "<i>No description available</i>"

    return sku_info

def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_full_name(username):
    result = subprocess.run(['net', 'user', username, '/domain'], capture_output=True, text=True)
    
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            if "Full Name" in line:
                return line.split("Full Name")[1].strip()
    else:
        return "Error: Could not fetch user information."

def readFileAsSoup(path):
    html_file= path

    with open(html_file, 'r', encoding='utf-8-sig') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    return soup,html_doc

def getGeneralInformation(soup):
    additional_details = soup.find('div', {'id': 'AdditionalDetails'})
    additional_text = additional_details.get_text(strip=True)

    recording_session = re.findall(r"Recording Session: (.*?)Recorded", additional_text)
    if len(recording_session) == 0:
            recording_session = re.findall(r"Aufzeichnungssitzung: (.*?)Aufgezeichnete", additional_text)
    recorded_steps = re.findall(r"Recorded Steps: (.*?),", additional_text)
    if len(recorded_steps) == 0:
            recorded_steps = re.findall(r"Aufgezeichnete Schritte: (.*?),", additional_text)
    missed_steps = re.findall(r"Missed Steps: (.*?),", additional_text)
    if len(missed_steps) == 0:
            missed_steps = re.findall(r"Nicht ausgeführte Schritte: (.*?),", additional_text)
    errors = re.findall(r"Other Errors: (.*?)Operating", additional_text)
    if len(errors) == 0:
            errors = re.findall(r"Andere Fehler: (.*?)Betriebssystem", additional_text)
    operating_system = re.findall(r"Operating System: (.*)Step 1:", additional_text)
    if len(operating_system) == 0:
            operating_system = re.findall(r"Betriebssystem: (.*)Schritt 1:", additional_text)

    script_tag = soup.find('script', {'id': 'myXML'})
    if script_tag:
        xml_data = script_tag.string.strip() 
        root = ET.fromstring(xml_data)
        system_tag = root.find('System')
        major = system_tag.get('MajorVersion')
        minor = system_tag.get('MinorVersion')
        service_major = system_tag.get('ServicePackMajor')
        service_minor = system_tag.get('ServicePackMinor')
        build = system_tag.get('BuildNumber')
        sku = system_tag.get('Sku')
        platform = system_tag.get('Platform')

        useraction_tag = root.find('UserActionData')
        session_tag = useraction_tag.find('RecordSession')
        
        general_information = {
            "recording_session": "",
            "recorded_steps": recorded_steps[0],
            "missed_steps": missed_steps[0],
            "errors": errors[0],
            "operating_system": operating_system[0],
            "os_major": major,
            "os_minor": minor,
            "os_service_major": service_major,
            "os_service_minor": service_minor,
            "os_build": build,
            "os_sku": sku,
            "os_platform": platform
        }

    return general_information

def getSteps(soup):
    steps_div = soup.find('div', {'id': 'Steps'})
    step_divs = steps_div.find_all('div', id=lambda x: x and 'Step' in x)

    script_tag = soup.find('script', {'id': 'myXML'})
    if script_tag:
        xml_data = script_tag.string.strip()  

        try:
            root = ET.fromstring(xml_data)

            user_action_data_tag = root.find('UserActionData')
            if user_action_data_tag is not None:

                each_actions = user_action_data_tag.findall('.//EachAction')  

                full_details_dict = {}
                for action in each_actions:
                    action_number = action.get('ActionNumber')
                    pid = action.get('Pid')
                    program_id = action.get('ProgramId')
                    file_id = action.get('FileId')
                    file_version = action.get('FileVersion')
                    file_description = action.get('FileDescription')
                    file_company = action.get('FileCompany')
                    file_name = action.get('FileName')
                    commandline = action.get('CommandLine')
                    description = action.find('Description').text
                    useraction = action.find('Action').text
                    cursor_coords = action.find('CursorCoordsXY').text
                    screen_coords = action.find('ScreenCoordsXYWH').text
                    screenshot = action.find('ScreenshotFileName').text

                    
                    uia_stack = action.find('UIAStack')
                    levels = []
                    if uia_stack is not None:
                        for level in uia_stack.findall('Level'):
                            level_details = {
                                'BoundingRectangle': level.get('BoundingRectangle'),
                                'ClassName': level.get('ClassName'),
                                'ControlType': level.get('ControlType'),
                                'FrameworkId': level.get('FrameworkId'),
                                'Name': level.get('Name'),
                                'LocalizedControlType': level.get('LocalizedControlType')
                            }
                            levels.append(level_details)

                    full_details_dict[action_number] = {
                        'useraction':useraction,
                        'pid': pid,
                        'program_id': program_id,
                        'file_id': file_id,
                        'file_version': file_version,
                        'file_description': file_description,
                        'file_company': file_company,
                        'file_name': file_name,
                        'commandline': commandline,
                        'description': description,
                        'cursor_coords': cursor_coords,
                        'screen_coords': screen_coords,
                        'screenshot': screenshot,
                        'uia_stack': levels  
                    }
            else:
                full_details_dict = {}

        except ET.ParseError as e:
            full_details_dict = {}
    else:
        full_details_dict = {}

    
    data = {}
    no_image = 0

    for div in step_divs:
        div_text = div.get_text(strip=True)

        step_info = re.search(r'Step (\d+): \((.*?)\)', div_text)
        if step_info == None:
            step_info = re.search(r'Schritt (\d+): \((.*?)\)', div_text)
        step_id = f'Step{step_info.group(1)}' if step_info else 'Step ID not found'

        timestamp = ''.join(c for c in step_info.group(2) if not unicodedata.category(c).startswith('C')) if step_info else 'Timestamp not found'
        titlepattern = r"Step.*? \d\d:\d\d:\d\d "
        title = re.sub(titlepattern, '', div.get('title'))
        image_name = ""
        try:
            image_name = div.img['src']
        except Exception as e:
            if "No screenshots were saved for this step." in str(div):
                image_name = "not_available.png"
                no_image = no_image + 1

        step_number = step_info.group(1)
        full_detail = full_details_dict.get(step_number, {})

        data[step_id] = {
            "title": title, 
            "timestamp": timestamp, 
            "image_name": image_name,
            "full_details": full_detail
        }

    return data, no_image

def writeOutputToJSON(data,general_information, path=""):
    output = {
        "general_information": general_information,
        "steps": data
    }
    
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    with open('tmp/output.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4,ensure_ascii=False)

def createVideo():
    frames = [Image.open(image) for image in glob.glob(f"out/Screenshots/*.JPEG")]
    frame_paths = [image.filename for image in frames]
    clip = ImageSequenceClip(frame_paths, fps=1000/700)
    if not os.path.exists("out/assets/"):
        os.makedirs("out/assets/")
    mp4_path = "out/assets/Recorded_Steps.mp4"
    clip.write_videofile(mp4_path, codec="libx264", fps=30, logger=None)

def extractImages(data):
    if not os.path.exists('out/Screenshots'):
        os.makedirs('out/Screenshots')
        
    matches = re.findall(r'Content-Location:\s(screenshot\d+.JPEG)\n\n(\/9j\/[\S\s]+?)(?=\-\-)', data)

    for m in matches:
        filename, img_data = m[0], m[1]
        img_data = ''.join(textwrap.wrap(img_data.replace('\n',''),2))
        imgdata = base64.b64decode(img_data)

        filepath = fr"out\Screenshots\{filename}"
        with open(filepath, 'wb') as f:
            f.write(imgdata)

def createHTML(no_image, json_file="tmp/output.json", template_file="template.html", output_file="out/Recording.html"):
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    shutil.rmtree('tmp')
    
    with open(template_file, 'r', encoding="utf-8") as f:
        template = f.read()

    json_data = json.dumps(data, indent=4)
    template = template.replace("<!-- Inline JSON data -->", f'<script id="json-data" type="application/json">{json_data}</script>')
    if not os.path.exists("out/assets"):
        os.makedirs("out/assets")
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(template)
        
    if no_image > 0:
        with open("not_available.png", 'rb') as f:
            not_available = f.read()
            with open("out/Screenshots/not_available.png", 'wb') as fo:
                fo.write(not_available)

def getConverterInformation(file_path):
    user = os.getlogin()
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    md5_hash = get_md5(file_path)
    file_size = os.path.getsize(file_path)/1024/1024
    file_size = float("{:.2f}".format(file_size))
    last_modified  = os.path.getmtime(file_path)
    last_modified = datetime.fromtimestamp(last_modified).strftime("%d.%m.%Y %H:%M:%S")

    return(user, current_time, md5_hash, file_size, last_modified)

def lookForMHT():
    rootDir = os.path.dirname(os.path.realpath(__file__))
    mht_files = glob.glob(os.path.join(rootDir, '*.mht'))
    if len(mht_files) != 1:
        print('No mht file found or more than one mht file found. Exiting now...')
        input('Press any key to continue...')
        exit()
    else:
        path = mht_files[0]
        return path.split("\\")[-1]

def main():
    path = lookForMHT()
    user, current_time, md5_hash, file_size, last_modified = getConverterInformation(path)
    soup, html_doc = readFileAsSoup(path)
    extractImages(html_doc)
    createVideo()
    general_information = getGeneralInformation(soup)
    general_information.update({
        "user": user,
        "current_time": current_time,
        "file_name": path,
        "md5": md5_hash,
        "file_size": file_size,
        "last_modified": last_modified
    })

    data, no_image = getSteps(soup)
    start, finish = data["Step1"]["timestamp"], data[f"Step{len(data)}"]["timestamp"]
    general_information.update({
        "recording_session": f"{start} - {finish}",
        "recording_start": start,
        "recording_finish": finish,
        "duration": calculate_time_difference(start, finish),
        "no_image": no_image
    })
    os_info = lookupSKU(int(general_information["os_sku"]), int(general_information["os_build"]))
    general_information.update({
        "os_edition": os_info['edition'],
        "os_description": os_info['description']
    })

    writeOutputToJSON(data, general_information)
    createHTML(no_image)
    os.startfile(os.path.join(os.getcwd(), "out", "Recording.html"))

if __name__ == '__main__':
    main()