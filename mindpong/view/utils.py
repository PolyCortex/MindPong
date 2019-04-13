from os.path import sep

from mindpong.utils import get_project_root

BACKGROUND_COLORS = {
    'GREEN': "background-color: #00a443",
    'RED': "background-color: #ff4141"
}

IMAGES_PATH = 'img_src'
MINDPONG_TITLE = 'MindPong'

def get_image_file(file_name):
    return sep.join([get_project_root(), IMAGES_PATH, file_name])
