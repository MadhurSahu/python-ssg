import os
import shutil
import sys

from src.generate_page import generate_pages_recursive


def main():
    basepath = sys.argv[0] if len(sys.argv) == 1 else "/"
    copy_static_data()
    generate_pages_recursive(basepath, "content", "template.html", "docs")


def copy_static_data():
    if not os.path.exists("static"):
        raise Exception("Static data directory doesn't exist")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copy_static_data_r("")


def copy_static_data_r(path):
    src = f"static/{path}"
    files = os.listdir(src)
    for file in files:
        file_path = os.path.join(src, file)
        dst_path = f"docs/{path}/{file}"
        if os.path.isfile(file_path):
            shutil.copy(file_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_static_data_r(path + "/" + file)
    return


if __name__ == '__main__':
    main()
