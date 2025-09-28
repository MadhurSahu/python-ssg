import os
import shutil


def main():
    copy_static_data()


def copy_static_data():
    if not os.path.exists("static"):
        raise Exception("Static data directory doesn't exist")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_static_data_r("")


def copy_static_data_r(path):
    src = f"static/{path}"
    files = os.listdir(src)
    for file in files:
        file_path = os.path.join(src, file)
        dst_path = f"public/{path}/{file}"
        if os.path.isfile(file_path):
            shutil.copy(file_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_static_data_r(path + "/" + file)
    return


if __name__ == '__main__':
    main()
