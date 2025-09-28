import os

from src.markdown_parser import markdown_to_html_node, extract_title


def generate_pages_recursive(dir_path_content, template_path, dest_path):
    files = os.listdir(dir_path_content)
    for file in files:
        file_path = os.path.join(dir_path_content, file)
        file_dst_path = os.path.join(dest_path, file.replace(".md", ".html"))
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, file_dst_path)
        else:
            generate_pages_recursive(file_path, template_path, file_dst_path)
    return


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page form {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()
    markdown_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", markdown_html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    open(dest_path, "w").write(template)
