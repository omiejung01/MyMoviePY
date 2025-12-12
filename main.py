import moviepy as mp
import os
from moviepy import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
from datetime import datetime

layout_list = ['2_01', '2_02', '2_03', '2_04', '3_01', '3_02', '3_03', '4_01']
http_finished_location = ''

def mix_sound(layout_name, video01_filename, video02_filename, delay01, delay02, volume01, volume02, owner_name):
    black_video_file_name = 'C:\\media\\mp4\\' + 'BlackVideo1Minute.mp4'
    black_video_file = VideoFileClip(black_video_file_name)
    black_video = black_video_file.with_effects([mp.video.fx.Resize(width=120)])

    outtro_video_file_name = 'C:\\media\\mp4\\' + 'FuzikScreen3Seconds.mp4'
    outtro_video_file = VideoFileClip(outtro_video_file_name).with_effects([mp.video.fx.Resize(width=120)])

    new_clip1 = VideoFileClip(video01_filename, fps_source='fps')
    new_clip2 = VideoFileClip(video02_filename, fps_source='fps')

    if delay01 > 0:
        black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
        black_video01 = black_video01.with_effects([mp.video.fx.Resize(width=120)])

        new_clip1 = concatenate_videoclips([black_video01, new_clip1])
        if volume01 != 1:
            new_clip1 = new_clip1.volumex(volume01)

    if delay02 > 0:
        black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
        black_video02 = black_video02.with_effects([mp.video.fx.Resize(width=120)])

        new_clip2 = concatenate_videoclips([black_video02, new_clip2])

        if volume02 != 1:
            new_clip2 = new_clip2.volumex(volume02)

    final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)), new_clip2.with_position((0, 0))],
                                    size=(192,108))

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")

    filename = str(owner_name + '_' + dt_string)

    video_filename = filename + "_108.mp4"
    sound_filename = filename + "_108.mp3"
    wave_filename = filename + "_wave.mp4"

    #final_clip.write_videofile(sound_filename, codec='mp3')
    final_clip.write_videofile(video_filename)

    MP4ToMP3(video_filename, sound_filename)

    cmd = "seewav -r 30 --width 1313 --height 341 --bar 120 --color \'200,200,0\' " + sound_filename + " " + wave_filename

    returned_value = os.system(cmd)

    return sound_filename

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
def merge_full(layout_name, video01_filename, video02_filename, delay01, delay02, volume01, volume02, owner_name):
    black_video_file_name = 'C:\\media\\mp4\\' + 'BlackVideo1Minute.mp4'
    black_video_file = VideoFileClip(black_video_file_name)
    black_video = black_video_file.with_effects([mp.video.fx.Resize(width=960)])

    outtro_video_file_name = 'C:\\media\\mp4\\' + 'FuzikScreen3Seconds.mp4'
    outtro_video_file = VideoFileClip(outtro_video_file_name)
    #outtro_video = outtro_video_file.resize(width=1920)

    outtro_video = outtro_video_file.with_effects([mp.video.fx.Resize(width=1920)])

    if layout_name == '2_01':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((607, 1080))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((1313, 738))])
        #new_clip2 = clip2.resize((1184, 664))

        if delay01 > 0:
            black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
            black_video01 = black_video01.with_effects([mp.video.fx.Resize((607, 1080))])

            new_clip1 = concatenate_videoclips([black_video01, new_clip1])
            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        if delay02 > 0:
            black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
            black_video02 = black_video02.with_effects([mp.video.fx.Resize((1313, 738))])

            new_clip2 = concatenate_videoclips([black_video02, new_clip2])

            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.with_position((0,0)) , new_clip2.with_position((608, 0))],
                                        size=(1920, 1080))

    if layout_name in layout_list:
    # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")

        filename = str(owner_name + '_' + dt_string)

        final_filename = filename + ".mp4"
            # final_clip.subclip('00:00:00.000', '00:00:10.000').resize(width=1920).write_videofile(final_filename)

            # final_clip.resize(width=1920).write_videofile(final_filename)

        video_url = http_finished_location + filename + ".mp4"

        # clip_preview = VideoFileClip(final_filename)
        if final_clip.duration < 10:
            print('Video clip must be longer than 10 seconds')
            auto_preview_frame = 2
            # return 'No video processing'
        else:
            if final_clip.duration < 15:
                auto_preview_frame = 5
            elif final_clip.duration < 25:
                auto_preview_frame = 15
            else:
                auto_preview_frame = 20

        final_clip.save_frame(final_filename.replace('.mp4', '.png'), t=auto_preview_frame)

        final_clip.with_effects([mp.video.fx.Resize(width=1920)])

        final_clip2 = concatenate_videoclips([final_clip, outtro_video])


        final_clip2.subclipped(0, 10).write_videofile(final_filename)
        final_clip.close()
        final_clip2.close()

        print(final_filename)
        print(final_filename.replace('.mp4', '.png'))

        """
        srv = pysftp.Connection(host=HOSTNAME, username=USERNAME,
                                    password=PASSWORD)

        #upload_filename = final_filename[final_filename.rindex('/') + 1:len(final_filename)]
        #print(upload_filename)

        with srv.cd(jam_location):  # chdir to public
            srv.put(final_filename)  # upload file to nodejs/

        with srv.cd(jam_location):  # chdir to public
            srv.put(final_filename.replace('.mp4','.png'))  # upload file to nodejs/

        # Closes the connection
        srv.close()
        """
    else:
        video_url = ''

    return video_url


def milli_to_timecode(millisecond):
    hour_digit = '00'
    min_digit = '00'
    second_digit = '00'
    milli_digit = '000'

    milli_digit = (millisecond % 1000)
    second_digit = ((millisecond - (millisecond % 1000)) / 1000) % 60
    min_digit = ((millisecond - (second_digit * 1000) - milli_digit) / 60000) % 60
    hour_digit = (millisecond - (min_digit * 60000) - (second_digit * 1000) - milli_digit) / 3600000

    # print (min_digit)
    display = ("{:0>2d}".format(int(hour_digit))) + ':' + ("{:0>2d}".format(int(min_digit))) + ':' + (
        "{:0>2d}".format(int(second_digit))) + '.' + ("{:0>3d}".format(milli_digit))

    return display


def create_seewav(input_filename, output_filename):
    input_file = VideoFileClip(input_filename)
    output = mp.video.fx.Margin(10, color=(255, 255, 255)).add_margin(input_file)
    #output.apply()
    #final_clip = input_file.Margin(60)

    output.write_videofile(output_filename, fps=60)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #create_seewav("in05.mp4","out05.mp4")
    #merge_full('2_01', 'C:\\media\\mp4\\Jazz-03-Saxophone-P.mp4' , 'C:\\media\\mp4\\Jazz-04-DoubleBass.mp4' , 0, 0, 1.0, 1.0, 'omiejung')
    mix_sound('2_01', 'C:\\media\\mp4\\Jazz-03-Saxophone-P.mp4' , 'C:\\media\\mp4\\Jazz-04-DoubleBass.mp4' , 0, 0, 1.0, 1.0, 'omiejung')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
