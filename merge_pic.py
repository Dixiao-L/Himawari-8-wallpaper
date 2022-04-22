from multiprocessing import Pool, cpu_count
from functools import partial
import PIL.Image as IM
from datetime import datetime, timedelta
import urllib.request as rq
import os

BASE_URL = 'https://himawari8.nict.go.jp/img/D531106/20d/550/'
ROW = 6
COL = 9
DATETIME = datetime.now() - timedelta(minutes=20)
DATE = DATETIME.strftime('%Y/%m/%d/')
TIME = f'{DATETIME.strftime("%H%M")[:-1]}000'
size = 550

def download_img(url, filePath):
    try:
        file_name = url.split('/')[-1]
        rq.urlretrieve(url, filename=f'{filePath}/{file_name}')
        print(" Downloaded {} ".format(file_name))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # filePath = os.path.dirname(os.path.abspath(__file__))
    filePath = './image'
    try:
        os.mkdir(filePath)
    except: pass
    urls = [f'{BASE_URL}{DATE}{TIME}_{j+1}_{i+1}.png' for i in range(ROW) for j in range(COL)]

    print("There are {} CPUs on this machine ".format(cpu_count()))
    pool = Pool(cpu_count())
    download_func = partial(download_img, filePath = filePath)
    results = pool.map(download_func, urls)
    pool.close()
    pool.join()

    to = IM.new('RGBA', (size*COL, size*ROW))

    for j in range(ROW):
        for i in range(COL):
            img = IM.open(f'{filePath}/{TIME}_{i+1}_{j+1}.png').resize((size, size))
            to.paste(img, ((i)*size, (j)*size))

    savePath = '/var/www/html'

    to.save(f'{savePath}/000.png')
