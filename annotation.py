import os
import time
import csv
import vlc
from blessed import Terminal

def fmt_time(t):
    m, s = divmod(t, 60)
    ms = (s - int(s)) * 1000  # get milliseconds
    return f"{int(m):02d}:{int(s):02d}:{int(ms):03d}"

def adjust_first_time(rows):
    rows[0][0] = '00:00:000'  # Update the start time of the first row
    return rows

def main():
    term = Terminal()
    label_map = {'1': '1', '2': '2', '3': '3'}
    playback_speed = 2.0
    videos = os.listdir('input_videos')

    for i, video in enumerate(videos):
        print(f"{i}: {video}\n")

    video_num = input("Choose a video by entering its number: ")
    video_name = videos[int(video_num)]
    annotation_filename = f"{os.path.splitext(video_name)[0]}.csv"

    print("Press 'p' to pause/resume.\nPress 'q' to quit.\n")

    player = vlc.MediaPlayer(os.path.join('input_videos', video_name))
    player.play()
    player.set_rate(playback_speed)
    time.sleep(1)  # Allow VLC to start playing video

    start = None
    label = None
    paused = False
    start_time = time.time()

    rows = []

    while True:
        with term.cbreak():
            key = term.inkey(timeout=0.1)

        if not paused:
            current_time = time.time()

        if key == 'p':
            if paused:
                paused = False
                player.play()
                start_time += time.time() - paused_time
            else:
                paused = True
                player.pause()
                paused_time = time.time()

        if key == 'q':
            if start is not None:
                end = fmt_time((current_time - start_time)*playback_speed)
                rows.append([start, end, label])
            break

        if str(key) in label_map:
            now = fmt_time((current_time - start_time)*playback_speed)
            if start is not None:
                rows.append([start, now, label])
            start = now
            label = label_map[str(key)]

    # Adjust the start time of the first row to be '00:00:000'
    rows = adjust_first_time(rows)

    with open(annotation_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    main()
