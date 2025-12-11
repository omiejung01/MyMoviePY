import moviepy as mp
from moviepy import VideoFileClip

layout_list = ['2_01', '2_02', '2_03', '2_04', '3_01', '3_02', '3_03', '4_01']
def merge_full(layout_name, video01_filename, video02_filename, delay01, delay02):
    if layout_name == '2_01':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        new_clip1 = clip1.resize((536, 1080))
        new_clip2 = clip2.resize((1184, 664))

        if delay01 > 0:
            black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
            new_clip1 = concatenate_videoclips([black_video01.resize((536, 1080)), clip1.resize((536, 1080))])
            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        if delay02 > 0:
            black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
            new_clip2 = concatenate_videoclips([black_video02.resize((1184, 664)), clip2.resize((1184, 664))])
            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.set_position((200, 0)), new_clip2.set_position((736, 272))],
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

        final_clip2 = concatenate_videoclips([final_clip.resize(width=1920), outtro_video])

        final_clip2.write_videofile(final_filename)
        final_clip.close()
        final_clip2.close()

        print(final_filename)
        print(final_filename.replace('.mp4', '.png'))

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
    create_seewav("in05.mp4","out05.mp4")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
