import argparse
import json
import os
from xml.etree import ElementTree

base_package_name = 'com.expensify.chat'

def update_build_gradle(suffix, build_gradle_path):
    with open(build_gradle_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("        applicationId "):
            lines[i] = f'        applicationId "{base_package_name}.{suffix}"\n'
            break

    with open(build_gradle_path, 'w') as f:
        f.writelines(lines)

def update_google_services_json(suffix, google_services_path):
    with open(google_services_path, 'r') as f:
        data = json.load(f)

    data['client'][0]['client_info']['android_client_info']['package_name'] = f'{base_package_name}.{suffix}'

    with open(google_services_path, 'w') as f:
        json.dump(data, f, indent=4)

def update_android_manifest(suffix, android_manifest_path):
    if not os.path.exists(android_manifest_path):
        return

    with open(android_manifest_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('package='):
            lines[i] = f'  package="{base_package_name}.{suffix}">\n'
            break

    with open(android_manifest_path, 'w') as f:
        f.writelines(lines)

def update_strings_xml(suffix, strings_xml_path):
    tree = ElementTree.parse(strings_xml_path)
    root = tree.getroot()

    for child in root:
        if child.attrib['name'] == "app_name":
            child.text = f'NE/{suffix}'
            break

    tree.write(strings_xml_path)

def main():
    parser = argparse.ArgumentParser(description="Update Android App ID with a given suffix.")
    parser.add_argument("suffix", help="The suffix to add to the app ID.")
    args = parser.parse_args()

    suffix = args.suffix

    base_path = 'android/app'
    build_gradle_path = os.path.join(base_path, 'build.gradle')
    google_services_path = os.path.join(base_path, 'google-services.json')
    strings_xml_path = os.path.join(base_path, 'src/main/res/values/strings.xml')
    android_manifest_path = os.path.join(base_path, 'src/main/AndroidManifest.xml')

    update_build_gradle(suffix, build_gradle_path)
    update_google_services_json(suffix, google_services_path)
    update_android_manifest(suffix, android_manifest_path)
    update_strings_xml(suffix, strings_xml_path)

if __name__ == "__main__":
    main()
