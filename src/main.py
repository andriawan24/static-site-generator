import os
import shutil
import blocks
import sys

basepath = sys.argv[1]

def get_directory(folder_name):
    print(basepath)
    return os.path.join(basepath, f"{folder_name}")

def check_directory_exists(directory):
    return os.path.exists(directory)

def copy_files(source, destination, files):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for file in files:
        file_path = os.path.join(source, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(destination, file))
        else:
            new_source = os.path.join(source, file)
            new_destination = os.path.join(destination, file)
            copy_files(new_source, new_destination, os.listdir(new_source))

def copy_static_dir():
    static_path = get_directory("static")
    public_path = get_directory("public")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    files_to_copy = os.listdir(static_path)
    copy_files(static_path, public_path, files_to_copy)

def extract_title(markdown):
    splitted = markdown.split('\n')
    for split in splitted:
        if split.startswith("# "):
            return split.lstrip("# ")
    raise ValueError("title is not valid")

def generate_page(from_path, dest_path, template_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}\n\n")

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    html_file = open(template_path)
    html_template = html_file.read()

    files = os.listdir(from_path)
    for file in files:
        file_path = os.path.join(from_path, file)

        if os.path.isfile(file_path):
            content_file = open(os.path.join(from_path, file))
            content = content_file.read()
            content_html = blocks.markdown_to_html_node(content).to_html()

            title = extract_title(content)
            new_html = html_template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
            new_html = new_html.replace("href=\"/", f"href=\"{basepath}")
            new_html = new_html.replace("src=\"/", f"src=\"{basepath}")

            dest_file = os.path.join(dest_path, 'index.html')
            new_html_file = open(dest_file, "x")
            new_html_file.write(new_html)

            content_file.close()
            new_html_file.close()
        else:
            new_source_path = os.path.join(from_path, file)
            new_destination_path = os.path.join(dest_path, file)
            generate_page(new_source_path, new_destination_path, template_path)

    html_file.close()

def main():

    copy_static_dir()
    source_path = os.path.join(basepath, "content")
    destination_path = os.path.join(basepath, "docs")
    template_path = os.path.join(basepath, "template.html")
    generate_page(source_path, destination_path, template_path)

main()
