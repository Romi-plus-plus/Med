from typing import Any


def _init_logger():
    import logging
    import colorlog

    logger = colorlog.getLogger("medtalk-kbqa")

    log_colors_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    # 输出到控制台
    console_handler = colorlog.StreamHandler()
    # 输出到文件
    file_handler = logging.FileHandler(filename="../medtalk-kbqa.log", mode='a', encoding='utf8')

    logger.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    # 日志输出格式
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s', log_colors=log_colors_config
    )
    file_formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', )

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)


    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    console_handler.close()
    file_handler.close()

    return logger


logger = _init_logger()


def colored(
    s: Any,
    *,
    fg: int | tuple[int, int, int] | None = None,
    bg: int | tuple[int, int, int] | None = None,
    bright: bool = False,
    underline: bool = False,
    flash: bool = False
) -> str:
    code: list[int] = []
    if bright:
        code.append(1)
    if underline:
        code.append(4)
    if flash:
        code.append(5)
    if isinstance(fg, int):
        code.append(30 + fg)
    elif isinstance(fg, tuple):
        code.extend([38, 2, *fg])
    if isinstance(bg, int):
        code.append(40 + bg)
    elif isinstance(bg, tuple):
        code.extend([48, 2, *bg])
    return f"\033[{';'.join(map(str, code))}m{s}\33[0m"


if __name__ == '__main__':
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')