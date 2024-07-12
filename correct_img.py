from pathlib import Path
import sys
from time import perf_counter, sleep
from PIL import Image, ImageDraw, ImageFont, ImageGrab, UnidentifiedImageError
from PIL.PyAccess import PyAccess
from PIL.ImageFilter import RankFilter, MinFilter, Kernel  # Kernel, DETAIL, SHARPEN


__version__ = '1.0.0'


def check_version() -> None:
    if sys.version_info < (3, 12, 0):
        print(u'Для работы требуется версия Python 3.9.7 и выше')
        sleep(4)
        sys.exit()
        raise Exception(u'Для работы требуется версия Python 3.9.7 и выше')


def thinning(img: Image.Image) -> Image.Image:
    # img = img.filter(Kernel((3,3), (1,1,1,1,-9,1,1,1,1), 2))
    # img = img.filter(RankFilter(3, 4))
    img = img.filter(MinFilter(3))
    return img


def correct(file_in: Path, num: int):
    start_time_screen = perf_counter()
    img = Image.open(file_in)

    img_corr = thinning(img)
    # file_out = file_in.parent / f'ocr_img{num}_correct_MinFilter.bmp'
    # img_corr.save(file_out, format='BMP', dpi=(100, 100))

    # img_corr = img.filter(RankFilter(3, 4))
    # img_corr = img_corr.filter(RankFilter(3, 4))
    # file_out = file_in.parent / f'ocr_img{num}_correct_RankFilter.bmp'
    # img_corr.save(file_out, format='BMP', dpi=(100, 100))

    # img_corr = img.filter(Kernel((3,3), (1,1,1,1,-9,1,1,1,1), 2))
    # file_out = file_in.parent / f'ocr_img{num}_correct_Kernel3-3.bmp'
    # img_corr.save(file_out, format='BMP', dpi=(100, 100))

    img_corr.save(file_in, format='BMP')

    print(f'Затрачено времени со скрином: {perf_counter() - start_time_screen}\n')


def main() -> None:
    nums = [3]  # test
    nums = [int(arg) for arg in sys.argv[1:]]

    PATH_SCRIPT = Path(__file__).parent
    for num in nums:
        file_in = PATH_SCRIPT / 'levels' / f'ocr_img{num}.bmp'
        correct(file_in, num)


if __name__ == '__main__':
    """python correct_img.py 1 2 3"""
    check_version()
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('Отмена. Скрипт остановлен.')
    except UnidentifiedImageError:
        print('Ошибка открытия файла изображения!')
    except OSError:
        print('Ошибка сохранения файла!')
    except Exception as e:
        print(f'Exception: {e}')  # __str__()
        raise e
        sys.exit(1)
