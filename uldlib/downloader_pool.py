from .const import CLI_STATUS_STARTLINE, DOWNPOSTFIX, DOWN_CHUNK_SIZE, CACHEPOSTFIX
# from . import utils
from .torrunner import TorRunner
from .segfile import SegFileLoader, SegFileMonitor
from .page import Page
import colors
import requests
import os
import sys
import multiprocessing as mp
import threading
import time
from datetime import timedelta
from types import FunctionType


class Downloader:
    # cli_initialized: bool
    # terminating: bool
    # processes: slice
    # captcha_process: mp.Process
    # captcha_solve_func: FunctionType
    # parts: int

    def __init__(self, captcha_solve_func, print_info_queue):
        self.captcha_solve_func = captcha_solve_func
        self.print_part_info_queue = print_info_queue
        self.terminating = False
        self.download_url_queue = mp.Queue(maxsize=0)
        self.processes = []
        self.captcha_process = None
        self.thread = None
        self.monitor = None

    def terminate(self):
        self.terminating = True

        print('Terminating download. Please wait for stopping all processes.')
        if hasattr(self, "captcha_process") and self.captcha_process is not None:
            self.captcha_process.terminate()
        print('Terminate download processes')
        if hasattr(self, "processes") and self.processes is not None:
            for p in self.processes:
                p.terminate()
        print('Download terminated.')
        if hasattr(self, "monitor") and self.monitor is not None:
            self.monitor.terminate()
        print('End download monitor')

    def _captcha_print_func_wrapper(self, text):
        pass
        # if not self.cli_initialized:
        #     sys.stdout.write(colors.blue(
        #         "[Link solve]\t") + text + "\033[K\r")
        # else:
        #     utils.print_captcha_status(text, self.parts)

    def _captcha_breaker(self):
        # utils.print_captcha_status(msg, parts)
        for url in self.captcha_download_links_generator:
            self.download_url_queue.put(url)

    @staticmethod
    def _save_progress(filename, parts, size, interval_sec):

        m = SegFileMonitor(filename, interval_sec)

        t_start = time.time()
        s_start = m.size()
        last_bps = [(s_start, t_start)]

        while True:
            time.sleep(interval_sec)
            s = m.size()
            t = time.time()

            total_bps = (s - s_start) / (t - t_start)

            # Average now bps for last 10 measurements
            if len(last_bps) >= 10:
                last_bps = last_bps[1:]
            (s_last, t_last) = last_bps[0]
            now_bps = (s - s_last) / (t - t_last)
            last_bps.append((s, t))

            remaining = (size - s) / total_bps if total_bps > 0 else 0

    @staticmethod
    def _download_part(part, download_url_queue, print_part_info_queue):
        """Download given part of the download.

            Arguments:
                part (dict): Specification of the part to download
        """

        idx = part.id
        print_part_info_queue.put(f"part {idx}", "text", "Starting download")
        print_part_info_queue.put(f"part {idx}", "size_total", part.size / 1024**2)

        part.started = time.time()
        part.now_downloaded = 0

        # Note the stream=True parameter
        r = requests.get(part.download_url, stream=True, allow_redirects=True, headers={
            "Range": "bytes={}-{}".format(part.pfrom + part.downloaded, part.pto),
            "Connection": "close",
        })

        if r.status_code == 429:
            print_part_info_queue.put(f"part {idx}", "text", f"Err {r.status_code}. Retrying")
            time.sleep(5)
            return Downloader._download_part(part, download_url_queue)

        if r.status_code != 206 and r.status_code != 200:
            print_part_info_queue.put(f"part {idx}", "text", f"Err {r.status_code}. Error")

        # reimplement as multisegment write file class
        for chunk in r.iter_content(chunk_size=DOWN_CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                part.write(chunk)
                part.now_downloaded += len(chunk)
                elapsed = time.time() - part.started

                # Print status line downloaded and speed
                # speed in bytes per second:
                speed = part.now_downloaded / elapsed if elapsed > 0 else 0
                # remaining time in seconds:
                remaining = (part.size - part.downloaded) / speed if speed > 0 else 0

                # utils.print_part_status(id, "{:.2f}%\t{:.2f}/{:.2f} MB\tspeed: {:.2f} KB/s\telapsed: {}\tremaining: {}".format(
                #     round(part.downloaded / part.size * 100, 2),
                #     round(part.downloaded / 1024**2,
                #           2), round(part.size / 1024**2, 2),
                #     round(speed / 1024, 2),
                #     str(timedelta(seconds=round(elapsed))),
                #     str(timedelta(seconds=round(remaining))),
                # ))

                print_part_info_queue.put(f"part {idx}", "size_curr", part.downloaded / 1024**2)
                print_part_info_queue.put(f"part {idx}", "speed_curr", speed / 1024)
                print_part_info_queue.put(f"part {idx}", "speed_avg", part.downloaded / 1024 / elapsed)
                print_part_info_queue.put(f"part {idx}", "elapsed", elapsed)
                print_part_info_queue.put(f"part {idx}", "remaining", remaining)

        # download end status
        r.close()
        part.elapsed = time.time() - part.started

        # utils.print_part_status(id, colors.green("Successfully downloaded {}{} MB in {} (speed {} KB/s)".format(
        #     round(part.now_downloaded / 1024**2, 2),
        #     "" if part.now_downloaded == part.downloaded else (
        #         "/"+str(round(part.downloaded / 1024**2, 2))
        #     ),
        #     str(timedelta(seconds=round(part.elapsed))),
        #     round(part.now_downloaded / part.elapsed / 1024, 2) if part.elapsed > 0 else 0
        # )))

        # close part file files
        part.close()

        # reuse download link if need
        download_url_queue.put(part.download_url)

    def download(self, url, parts=10, target_dir=""):
        """Download file from Uloz.to using multiple parallel downloads.
            Arguments:
                url (str): URL of the Uloz.to file to download
                parts (int): Number of parts that will be downloaded in parallel (default: 10)
                target_dir (str): Directory where the download should be saved (default: current directory)
        """
        self.url = url
        self.parts = parts
        self.processes = []
        self.captcha_process = None
        self.target_dir = target_dir
        self.terminating = False
        self.isLimited = False
        self.isCaptcha = False

        started = time.time()
        previously_downloaded = 0

        # 1. Prepare downloads
        # print("Starting downloading for url '{}'".format(url))
        # # 1.1 Get all needed information
        # print("Getting info (filename, filesize, ...)")

        try:
            tor = TorRunner()
            page = Page(url, target_dir, parts, tor)
            page.parse()

        except RuntimeError as e:
            self.download(url, parts, target_dir)
            sys.exit(1)

        # Do check - only if .udown status file not exists get question
        output_filename = os.path.join(target_dir, page.filename)

        # if os.path.isfile(output_filename) and not os.path.isfile(output_filename+DOWNPOSTFIX):
        #     print(colors.yellow(
        #         "WARNING: File '{}' already exists, overwrite it? [y/n] ".format(output_filename)), end="")
        #     if input().strip() != 'y':
        #         sys.exit(1)

        if page.quickDownloadURL is not None:
            # print("You are VERY lucky, this is QUICK direct download without CAPTCHA, downloading as 1 quick part :)")
            self.download_type = "fullspeed direct download (without CAPTCHA)"
            download_url = page.quickDownloadURL
            self.captcha_solve_func = None

        if page.slowDownloadURL is not None:
            self.isLimited = True
            if page.isDirectDownload:
                # print("You are lucky, this is slow direct download without CAPTCHA :)")
                self.download_type = "slow direct download (without CAPTCHA)"
            else:
                self.isCaptcha = True
                # print("CAPTCHA protected download - CAPTCHA challenges will be displayed\n")
                self.download_type = "CAPTCHA protected download"

            self.captcha_download_links_generator = page.captcha_download_links_generator(
                captcha_solve_func=self.captcha_solve_func,
                print_func=self._captcha_print_func_wrapper
            )
            download_url = next(self.captcha_download_links_generator)

        head = requests.head(download_url, allow_redirects=True)
        total_size = int(head.headers['Content-Length'])

        try:
            file_data = SegFileLoader(output_filename, total_size, parts)
            downloads = file_data.make_writers()
        except Exception as e:
            print(colors.red(f"Failed: Can not create '{output_filename}' error: {e} "))
            self.terminate()
            sys.exit()

        # 2. Initialize cli status table interface
        # if windows, use 'cls', otherwise use 'clear'

        # os.system('cls' if os.name == 'nt' else 'clear')
        # sys.stdout.write("\033[?25l")  # hide cursor
        # self.cli_initialized = True

        page.cli_initialized = True  # for tor in Page

        # print(colors.blue("File:\t\t") + colors.bold(page.filename))
        # print(colors.blue("URL:\t\t") + page.url)
        # print(colors.blue("Download type:\t") + self.download_type)
        # print(colors.blue("Size / parts: \t") +
        #       colors.bold(f"{round(total_size / 1024**2, 2)}MB => " +
        #       f"{file_data.parts} x {round(file_data.part_size / 1024**2, 2)}MB"))

        self.print_part_info_queue.put("filename", "text", page.filename)
        self.print_part_info_queue.put("url", "text", page.url)
        self.print_part_info_queue.put("download type", "text", self.download_type)
        self.print_part_info_queue.put("file parts", "text", f"{file_data.parts} x {file_data.part_size / 1024**2:.2f} MB => {total_size / 1024**2:.2f} MB")

        # fill placeholder before download started
        for part in downloads:
            idx = part.id
            if page.isDirectDownload:
                self.print_part_info_queue.put(f"part {idx}", "text", "Waiting for direct link")
                # utils.print_part_status(part.id, "Waiting for direct link...")
            else:
                self.print_part_info_queue.put(f"part {idx}", "text", "Waiting for CAPTCHA")
                # utils.print_part_status(part.id, "Waiting for CAPTCHA...")

        # Prepare queue for recycling download URLs
        self.download_url_queue = mp.Queue(maxsize=0)

        # limited must use TOR and solve links or captcha
        if self.isLimited:
            # Reuse already solved links
            self.download_url_queue.put(download_url)

            # Start CAPTCHA breaker in separate process
            self.captcha_process = mp.Process(
                target=self._captcha_breaker, args=(page, self.parts)
            )

        cpb_started = False
        page.alreadyDownloaded = 0

        # save status monitor
        self.monitor = mp.Process(target=Downloader._save_progress, args=(
            file_data.filename, file_data.parts, file_data.size, 1/3))
        self.monitor.start()

        # 3. Start all downloads fill self.processes
        for part in downloads:
            if self.terminating:
                return
            idx = part.id

            if part.downloaded == part.size:
                # utils.print_part_status(id, colors.green(
                #     "Already downloaded from previous run, skipping"))
                self.print_part_info_queue.put(f"part {idx}", "text", "Already downloaded")
                self.print_part_info_queue.put(f"part {idx}", "percentage", "100")

                page.alreadyDownloaded += 1
                continue

            if self.isLimited:
                if not cpb_started:
                    self.captcha_process.start()
                    cpb_started = True
                part.download_url = self.download_url_queue.get()
            else:
                part.download_url = download_url

            # Start download process in another process (parallel):
            p = mp.Process(target=Downloader._download_part,
                           args=(part, self.download_url_queue, self.print_part_info_queue))
            p.start()
            self.processes.append(p)

        if self.isLimited:
            # no need for another CAPTCHAs
            self.captcha_process.terminate()
            # if self.isCaptcha:
            #     utils.print_captcha_status(
            #         "All downloads started, no need to solve another CAPTCHAs..", self.parts)
            # else:
            #     utils.print_captcha_status(
            #         "All downloads started, no need to solve another direct links..", self.parts)

        # 4. Wait for all downloads to finish
        success = True
        for p in self.processes:
            p.join()
            if p.exitcode != 0:
                success = False

        # clear cli
        sys.stdout.write("\033[{};{}H".format(
            parts + CLI_STATUS_STARTLINE + 2, 0))
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[?25h")  # show cursor
        self.cli_initialized = False

        # result end status
        if not success:
            print(colors.red("Failure of one or more downloads, exiting"))
            sys.exit(1)

        elapsed = time.time() - started
        # speed in bytes per second:
        speed = (total_size - previously_downloaded) / elapsed if elapsed > 0 else 0
        print(colors.green("All downloads finished"))
        print("Stats: Downloaded {}{} MB in {} (average speed {} MB/s)".format(
            round((total_size - previously_downloaded) / 1024**2, 2),
            "" if previously_downloaded == 0 else (
                "/"+str(round(total_size / 1024**2, 2))
            ),
            str(timedelta(seconds=round(elapsed))),
            round(speed / 1024**2, 2)
        ))
        # remove resume .udown file
        udown_file = output_filename + DOWNPOSTFIX
        if os.path.exists(udown_file):
            print(f"Delete file: {udown_file}")
            os.remove(udown_file)
        # remove .ucache file
        ucache_file = output_filename + CACHEPOSTFIX
        if os.path.exists(ucache_file):
            print(f"Delete file: {ucache_file}")
            os.remove(ucache_file)

    def download_thread(self, url, parts=10, target_dir=""):
        self.thread = threading.Thread(target=self.download, args=(url, parts, target_dir))
        self.thread.start()

    def join(self):
        if self.thread is not None:
            self.thread.join()

