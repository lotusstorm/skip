import re
import socket

PATH = 'src/store/globalSettings.js'


def change_ip(path):
    """

    :param path:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()

    with open(path, 'r') as inp:
        text = inp.read()
        pattern = re.compile(r'http://(.*?):')
        out_text = re.sub(re.search(pattern, text).group(1), ip, text)

        with open(path, 'w') as out:
            out.write(out_text)


if __name__ == '__main__':
    change_ip(PATH)
