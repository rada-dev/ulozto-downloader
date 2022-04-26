#!/usr/bin/env python3
"""Uloz.to quick multiple sessions downloader."""
import urwid as uw
from uldlib import downloader_pool, captcha
from uldui import app, frame

import multiprocessing
import signal
import sys
import os


def main():
    def sigint_handler(sig, fr):
        raise uw.ExitMainLoop
    signal.signal(signal.SIGINT, sigint_handler)

    model_path = os.path.join("uldlib", "model.tflite")
    model_download_url = "https://github.com/JanPalasek/ulozto-captcha-breaker/releases/download/v2.2/model.tflite"
    captcha_solve_fnc = captcha.AutoReadCaptcha(model_path, model_download_url)

    print_part_info_queue = multiprocessing.Queue(maxsize=0)

    url = "https://ulozto.cz/file/ypZ91KycjCle/shrek-1-cz-en-1080p-mkv#!ZGp4LGR2ZJR2AzMzAzZ1MQOuAwAuZ2IfD2b4K0S3BQShZQR4AN=="
    parts = 10
    output = ""
    d = downloader_pool.Downloader(captcha_solve_fnc, print_part_info_queue)
    d.download(url, parts, output)
    w = frame.UldFrame(print_part_info_queue)
    a = app.App(w)

    a.start()
    a.join()


if __name__ == "__main__":
    main()
