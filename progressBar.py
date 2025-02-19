import sys

def progress_bar_downloading(iteration, total, speed, elapsed_time, prefix='', suffix='', bar_length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = fill * filled_length + '-' * (bar_length - filled_length)

    downloaded_mb = iteration / (1024 * 1024)
    total_mb = total / (1024 * 1024)

    if speed >= 1024:
        speed_display = f"{speed / 1024:.2f} MB/s"
    else:
        speed_display = f"{speed:.2f} kB/s"

    sys.stdout.write(f'\r{prefix:<10} [{downloaded_mb:.2f} MB/{total_mb:.2f} MB  {speed_display}  {elapsed_time:.2f}s] |{bar}| {percent}% - {suffix}')
    sys.stdout.flush()

def progress_bar_unzipping(iteration, total, speed, elapsed_time, prefix='', suffix='', bar_length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = fill * filled_length + '-' * (bar_length - filled_length)

    if speed >= 1024:
        speed_display = f"{speed / 1024:.2f} MB/s"
    else:
        speed_display = f"{speed:.2f} kB/s"
    
    minutes, seconds = divmod(elapsed_time, 60)
    elapsed_formatted = f"{int(minutes)}m {int(seconds)}s" if minutes > 0 else f"{elapsed_time:.2f}s"

    sys.stdout.write(f'\r{prefix:<12} [{iteration}/{total}] {percent}% |{bar}| {speed_display}  {elapsed_formatted}     {suffix}')
    sys.stdout.flush()