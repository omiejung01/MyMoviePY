import moviepy as mp
import os
from moviepy import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, ColorClip, TextClip, ImageClip
from datetime import datetime

layout_list = ['2_01', '2_02', '2_03', '2_04', '2_05', '2_06', '2_07', '2_08',
               '3_01', '3_02', '3_03', '3_04', '3_05', '3_06', '3_07', '4_01']
http_finished_location = ''

def AlphaVideo():
    canvas_size = (1920, 1080)

    # 2. Create your content (e.g., a TextClip)
    # We ensure the text is centered and has a transparent background
    txt_clip = TextClip(
        text="Transparent Video",
        font_size=150,
        color='white',
        font="Arial",  # Ensure this font is installed on your system
        duration=5
    ).with_position('center')

    # 3. Create the final composition
    # We don't add a background clip so the empty space stays transparent
    final_clip = CompositeVideoClip([txt_clip], size=canvas_size)
    final_clip = final_clip.with_duration(5)

    return final_clip


def gen_sound(video01_filename, volume01, owner_name):
    new_clip1 = VideoFileClip(video01_filename, fps_source='fps')
    final_clip = CompositeVideoClip([new_clip1.with_position((0, 0))],
                                    size=(192, 108))
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")

    filename = str(owner_name + '_' + dt_string)

    video_filename = filename + "_108.mp4"
    sound_filename = filename + "_108.mp3"
    wave_filename = filename + "_wave.mp4"

    # final_clip.write_videofile(sound_filename, codec='mp3')
    final_clip.write_videofile(video_filename)

    MP4ToMP3(video_filename, sound_filename)

    cmd = "seewav -r 30 --width 960 --height 540 --bar 120 --color 1,1,0 " + sound_filename + " " + wave_filename

    returned_value = os.system(cmd)

    return wave_filename
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

    cmd = "seewav -r 30 --width 960 --height 540 --bar 120 --color 1,1,0 " + sound_filename + " " + wave_filename

    returned_value = os.system(cmd)

    return wave_filename

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
def merge_full(layout_name, video01_filename, video02_filename, video03_filename, video04_filename,
               delay01, delay02, delay03, delay04,
               volume01, volume02, volume03, volume04,
               owner_name):
    black_video_file_name = 'C:\\media\\mp4\\' + 'BlackVideo1Minute.mp4'
    black_video_file = VideoFileClip(black_video_file_name)
    black_video = black_video_file.with_effects([mp.video.fx.Resize(width=960)])

    alpha_video_file_name = 'C:\\media\\mp4\\' + 'AlphaVideo.mp4'
    alpha_video_file = VideoFileClip(alpha_video_file_name, is_mask=True, has_mask=False)
    alpha_video = alpha_video_file.with_effects([mp.video.fx.Resize(width=1920)])

    outtro_video_file_name = 'C:\\media\\mp4\\' + 'FuzikScreen3Seconds.mp4'
    outtro_video_file = VideoFileClip(outtro_video_file_name)
    #outtro_video = outtro_video_file.resize(width=1920)

    outtro_video = outtro_video_file.with_effects([mp.video.fx.Resize(width=1920)])

    if layout_name == '2_01':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        total_duration01 = (clip1.duration * 1000) + delay01  # millisecond
        total_duration02 = (clip2.duration * 1000) + delay02  # millisecond

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((1910, 1070))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((630, 350))])

        new_clip1 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip1)
        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        if delay01 > 0:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
        else:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)

        if volume01 != 1:
            new_clip1 = new_clip1.volumex(volume01)

        # Clip 02
        if delay02 > 0:
            new_clip2 = mp.video.fx.CrossFadeIn(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeIn(2).apply(new_clip2)

        if total_duration01 >= total_duration02:
            new_clip2 = mp.video.fx.CrossFadeOut(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeOut(2).apply(new_clip2)
        if volume02 != 1:
            new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)).with_start(milli_to_timecode(delay01)),
                                         new_clip2.with_position((100, 620)).with_start(milli_to_timecode(delay02))],
                                        is_mask=False,
                                        size=(1920, 1080))
    if layout_name == '2_02':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        total_duration01 = (clip1.duration * 1000) + delay01  # millisecond
        total_duration02 = (clip2.duration * 1000) + delay02  # millisecond

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((1910, 1070))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((630, 350))])

        new_clip1 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip1)
        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        if delay01 > 0:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
        else:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)

        if volume01 != 1:
            new_clip1 = new_clip1.volumex(volume01)

        # Clip 02
        if delay02 > 0:
            new_clip2 = mp.video.fx.CrossFadeIn(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeIn(2).apply(new_clip2)

        if total_duration01 >= total_duration02:
            new_clip2 = mp.video.fx.CrossFadeOut(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeOut(2).apply(new_clip2)
        if volume02 != 1:
            new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)).with_start(milli_to_timecode(delay01)),
                                         new_clip2.with_position((100, 60)).with_start(milli_to_timecode(delay02))],
                                        is_mask=False,
                                        size=(1920, 1080))
    if layout_name == '2_03':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        total_duration01 = (clip1.duration * 1000) + delay01  # millisecond
        total_duration02 = (clip2.duration * 1000) + delay02  # millisecond

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((1910, 1070))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((630, 350))])

        new_clip1 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip1)
        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        if delay01 > 0:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
        else:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)

        if volume01 != 1:
            new_clip1 = new_clip1.volumex(volume01)

        # Clip 02
        if delay02 > 0:
            new_clip2 = mp.video.fx.CrossFadeIn(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeIn(2).apply(new_clip2)

        if total_duration01 >= total_duration02:
            new_clip2 = mp.video.fx.CrossFadeOut(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeOut(2).apply(new_clip2)
        if volume02 != 1:
            new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)).with_start(milli_to_timecode(delay01)),
                                         new_clip2.with_position((1190, 60)).with_start(milli_to_timecode(delay02))],
                                        is_mask=False,
                                        size=(1920, 1080))

    if layout_name == '2_04':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        total_duration01 = (clip1.duration * 1000) + delay01  # millisecond
        total_duration02 = (clip2.duration * 1000) + delay02  # millisecond

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((1910, 1070))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((630, 350))])

        new_clip1 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip1)
        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        if delay01 > 0:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
        else:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)

        if volume01 != 1:
            new_clip1 = new_clip1.volumex(volume01)

        # Clip 02
        if delay02 > 0:
            new_clip2 = mp.video.fx.CrossFadeIn(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeIn(2).apply(new_clip2)

        if total_duration01 >= total_duration02:
            new_clip2 = mp.video.fx.CrossFadeOut(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeOut(2).apply(new_clip2)
        if volume02 != 1:
            new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)).with_start(milli_to_timecode(delay01)),
                                         new_clip2.with_position((1190, 620)).with_start(milli_to_timecode(delay02))],
                                        is_mask=False,
                                        size=(1920, 1080))

    if layout_name == '2_05':

        image_2_05_top_filename = 'C:\\media\images\\2_05_top.png'
        image_2_05_bottom_filename = 'C:\\media\images\\2_05_bottom.png'

        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        Image205Top = ImageClip(image_2_05_top_filename)
        Image205Top = Image205Top.with_start(0).with_duration(clip1.duration)

        # Position the image clip in the center of the screen
        Image205Top = Image205Top.with_effects([mp.video.fx.Resize((100, 100))]).with_position((20, 20))

        Image205Bottom = ImageClip(image_2_05_bottom_filename)
        Image205Bottom = Image205Bottom.with_start(0).with_duration(clip2.duration)

        # Position the image clip in the center of the screen
        Image205Bottom = Image205Bottom.with_effects([mp.video.fx.Resize((100, 100))]).with_position((20, 20))
        # Combine the video and the image overlay into a single clip

        # x 950
        # y 530

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((950, 530))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((950, 535))])
        #new_clip2 = clip2.resize((1184, 664))

        if delay01 > 0:
            black_video01 = black_video.subclipped('00:00:00.000', milli_to_timecode(delay01))
            black_video01 = black_video01.with_effects([mp.video.fx.Resize((950, 530))])
            new_clip1 = concatenate_videoclips([black_video01, new_clip1])

            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        new_clip1 = mp.video.fx.Margin(top=5, left=5, right=5, color=(255, 255, 0)).add_margin(new_clip1)

        if delay02 > 0:
            black_video02 = black_video.subclipped('00:00:00.000', milli_to_timecode(delay02))
            black_video02 = black_video02.with_effects([mp.video.fx.Resize((950, 535))])
            new_clip2 = concatenate_videoclips([black_video02, new_clip2])

            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        wave01 = gen_sound(video01_filename, volume01, owner_name)

        wav01_clip = VideoFileClip(wave01, fps_source='fps')
        wav01_clip2 = wav01_clip.with_volume_scaled(0.0)
        wav01_clip3 = wav01_clip2.with_effects([mp.video.fx.Resize((955, 355))])
        wav01_clip4 = mp.video.fx.Margin(top=5,  right=5, color=(255, 255, 0)).add_margin(wav01_clip3)

        wav01_clip4 = CompositeVideoClip([wav01_clip4, Image205Top])

        wave02 = gen_sound(video02_filename, volume02, owner_name)

        wav02_clip = VideoFileClip(wave02, fps_source='fps')
        wav02_clip2 = wav02_clip.with_volume_scaled(0.0)
        wav02_clip3 = wav02_clip2.with_effects([mp.video.fx.Resize((955, 355))])
        wav02_clip4 = mp.video.fx.Margin(top=5, right=5, color=(255, 255, 0)).add_margin(wav02_clip3)

        wav02_clip4 = CompositeVideoClip([wav02_clip4, Image205Bottom])

        wave_file = mix_sound(layout_name, video01_filename, video02_filename, delay01, delay02, volume01, volume02, owner_name)

        final_wav_clip = VideoFileClip(wave_file, fps_source='fps')
        final_wav_clip2 = final_wav_clip.with_volume_scaled(0.0)
        final_wav_clip3 = final_wav_clip2.with_effects([mp.video.fx.Resize((955, 350))])
        final_wav_clip4 = mp.video.fx.Margin(top=5, bottom=5, right=5, color=(255, 255, 0)).add_margin(final_wav_clip3)

        #final_clip = CompositeVideoClip([new_clip1.with_position((0,0)), new_clip2.with_position((613, 0)), wav_clip4.with_position((613,743))],
        #                                size=(1920, 1080))

        # 5 + 355 + 5 + 355 + 5 + 350 + 5
        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)), new_clip2.with_position((0, 535)),
                                         wav01_clip4.with_position((960, 0)), wav02_clip4.with_position((960, 360)),
                                         final_wav_clip4.with_position((960, 720))],
                                        size=(1920, 1080))

    if layout_name == '2_06':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((603, 1070))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((1302, 733))])
        #new_clip2 = clip2.resize((1184, 664))

        if delay01 > 0:
            black_video01 = black_video.subclipped('00:00:00.000', milli_to_timecode(delay01))
            black_video01 = black_video01.with_effects([mp.video.fx.Resize((603, 1070))])
            new_clip1 = concatenate_videoclips([black_video01, new_clip1])

            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        new_clip1 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip1)

        if delay02 > 0:
            black_video02 = black_video.subclipped('00:00:00.000', milli_to_timecode(delay02))
            black_video02 = black_video02.with_effects([mp.video.fx.Resize((1302, 733))])
            new_clip2 = concatenate_videoclips([black_video02, new_clip2])

            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        new_clip2 = mp.video.fx.Margin(top=5,right=5, bottom=5, color=(255, 255, 0)).add_margin(new_clip2)
        wave_file = mix_sound(layout_name, video01_filename, video02_filename, delay01, delay02, volume01, volume02, owner_name)

        wav_clip = VideoFileClip(wave_file, fps_source='fps')
        wav_clip2 = wav_clip.with_volume_scaled(0.0)
        wav_clip3 = wav_clip2.with_effects([mp.video.fx.Resize((1302, 332))])
        wav_clip4 = mp.video.fx.Margin(bottom=5, right=5, color=(255, 255, 0)).add_margin(wav_clip3)

        final_clip = CompositeVideoClip([new_clip1.with_position((0,0)), new_clip2.with_position((613, 0)), wav_clip4.with_position((613,743))],
                                        size=(1920, 1080))

    if layout_name == '2_07':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        total_duration01 = (clip1.duration * 1000) + delay01  # millisecond
        total_duration02 = (clip2.duration * 1000) + delay02  # millisecond

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((1910, 1070))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((350, 630))])

        new_clip1 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip1)
        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        if delay01 > 0:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
        else:
            if total_duration01 >= total_duration02:
                new_clip1 = mp.video.fx.FadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.FadeOut(2).apply(new_clip1)
            else:
                new_clip1 = mp.video.fx.CrossFadeIn(2).apply(new_clip1)
                new_clip1 = mp.video.fx.CrossFadeOut(2).apply(new_clip1)

        if volume01 != 1:
            new_clip1 = new_clip1.volumex(volume01)

        # Clip 02
        if delay02 > 0:
            new_clip2 = mp.video.fx.CrossFadeIn(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeIn(2).apply(new_clip2)

        if total_duration01 >= total_duration02:
            new_clip2 = mp.video.fx.CrossFadeOut(2).apply(new_clip2)
        else:
            new_clip2 = mp.video.fx.FadeOut(2).apply(new_clip2)
        if volume02 != 1:
            new_clip2 = new_clip2.volumex(volume02)

        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)).with_start(milli_to_timecode(delay01)),
                                         new_clip2.with_position((1490, 380)).with_start(
                                             milli_to_timecode(delay02))],
                                        is_mask=False,
                                        size=(1920, 1080))

    if layout_name == '2_08':

        image_2_08_left_filename = 'C:\\media\images\\2_08_left.png'
        image_2_08_right_filename = 'C:\\media\images\\2_08_right.png'

        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')

        Image205Top = ImageClip(image_2_05_top_filename)
        Image205Top = Image205Top.with_start(0).with_duration(clip1.duration)

        # Position the image clip in the center of the screen
        Image205Top = Image205Top.with_effects([mp.video.fx.Resize((100, 100))]).with_position((20, 20))

        Image205Bottom = ImageClip(image_2_05_bottom_filename)
        Image205Bottom = Image205Bottom.with_start(0).with_duration(clip2.duration)

        # Position the image clip in the center of the screen
        Image205Bottom = Image205Bottom.with_effects([mp.video.fx.Resize((100, 100))]).with_position((20, 20))
        # Combine the video and the image overlay into a single clip

        # x 950
        # y 530

        new_clip1 = clip1.with_effects([mp.video.fx.Resize((950, 530))])
        new_clip2 = clip2.with_effects([mp.video.fx.Resize((950, 535))])
        # new_clip2 = clip2.resize((1184, 664))

        if delay01 > 0:
            black_video01 = black_video.subclipped('00:00:00.000', milli_to_timecode(delay01))
            black_video01 = black_video01.with_effects([mp.video.fx.Resize((950, 530))])
            new_clip1 = concatenate_videoclips([black_video01, new_clip1])

            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        new_clip1 = mp.video.fx.Margin(top=5, left=5, right=5, color=(255, 255, 0)).add_margin(new_clip1)

        if delay02 > 0:
            black_video02 = black_video.subclipped('00:00:00.000', milli_to_timecode(delay02))
            black_video02 = black_video02.with_effects([mp.video.fx.Resize((950, 535))])
            new_clip2 = concatenate_videoclips([black_video02, new_clip2])

            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        new_clip2 = mp.video.fx.Margin(5, color=(255, 255, 0)).add_margin(new_clip2)

        wave01 = gen_sound(video01_filename, volume01, owner_name)

        wav01_clip = VideoFileClip(wave01, fps_source='fps')
        wav01_clip2 = wav01_clip.with_volume_scaled(0.0)
        wav01_clip3 = wav01_clip2.with_effects([mp.video.fx.Resize((955, 355))])
        wav01_clip4 = mp.video.fx.Margin(top=5, right=5, color=(255, 255, 0)).add_margin(wav01_clip3)

        wav01_clip4 = CompositeVideoClip([wav01_clip4, Image205Top])

        wave02 = gen_sound(video02_filename, volume02, owner_name)

        wav02_clip = VideoFileClip(wave02, fps_source='fps')
        wav02_clip2 = wav02_clip.with_volume_scaled(0.0)
        wav02_clip3 = wav02_clip2.with_effects([mp.video.fx.Resize((955, 355))])
        wav02_clip4 = mp.video.fx.Margin(top=5, right=5, color=(255, 255, 0)).add_margin(wav02_clip3)

        wav02_clip4 = CompositeVideoClip([wav02_clip4, Image205Bottom])

        wave_file = mix_sound(layout_name, video01_filename, video02_filename, delay01, delay02, volume01, volume02,
                              owner_name)

        final_wav_clip = VideoFileClip(wave_file, fps_source='fps')
        final_wav_clip2 = final_wav_clip.with_volume_scaled(0.0)
        final_wav_clip3 = final_wav_clip2.with_effects([mp.video.fx.Resize((955, 350))])
        final_wav_clip4 = mp.video.fx.Margin(top=5, bottom=5, right=5, color=(255, 255, 0)).add_margin(final_wav_clip3)

        # final_clip = CompositeVideoClip([new_clip1.with_position((0,0)), new_clip2.with_position((613, 0)), wav_clip4.with_position((613,743))],
        #                                size=(1920, 1080))

        # 5 + 355 + 5 + 355 + 5 + 350 + 5
        final_clip = CompositeVideoClip([new_clip1.with_position((0, 0)), new_clip2.with_position((0, 535)),
                                         wav01_clip4.with_position((960, 0)), wav02_clip4.with_position((960, 360)),
                                         final_wav_clip4.with_position((960, 720))],
                                        size=(1920, 1080))


    if layout_name == '3_01':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')
        clip3 = VideoFileClip(video03_filename, fps_source='fps')

        new_clip1 = clip1.resize((536, 1080))
        new_clip2 = clip2.resize((960, 540))
        new_clip3 = clip3.resize((960, 540))

        if delay01 > 0:
            black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
            new_clip1 = concatenate_videoclips([black_video01.resize((536, 1080)), clip1.resize((536, 1080))])
            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        if delay02 > 0:
            black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
            new_clip2 = concatenate_videoclips([black_video02.resize((960, 540)), clip2.resize((960, 540))])
            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        if delay03 > 0:
            black_video03 = black_video.subclip('00:00:00.000', milli_to_timecode(delay03))
            new_clip3 = concatenate_videoclips([black_video03.resize((960, 540)), clip3.resize((960, 540))])
            if volume03 != 1:
                new_clip3 = new_clip3.volumex(volume03)

        final_clip = CompositeVideoClip(
            [new_clip1.set_position((424, 0)), new_clip2.set_position((960, 0)),
             new_clip3.set_position((960, 540))],
            size=(1920, 1080))

    if layout_name == '3_02':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')
        clip3 = VideoFileClip(video03_filename, fps_source='fps')

        new_clip1 = clip1.resize((960, 540))
        new_clip2 = clip2.resize((960, 540))
        new_clip3 = clip3.resize((960, 540))

        if delay01 > 0:
            black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
            new_clip1 = concatenate_videoclips([black_video01, clip1.resize((960, 540))])
            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        if delay02 > 0:
            black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
            new_clip2 = concatenate_videoclips([black_video02, clip2.resize((960, 540))])
            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        if delay03 > 0:
            black_video03 = black_video.subclip('00:00:00.000', milli_to_timecode(delay03))
            new_clip3 = concatenate_videoclips([black_video03, clip3.resize((960, 540))])
            if volume03 != 1:
                new_clip3 = new_clip3.volumex(volume03)

        final_clip = CompositeVideoClip(
            [new_clip1.set_position((0, 0)), new_clip2.set_position((960, 0)),
             new_clip3.set_position((480, 540))],
            size=(1920, 1080))

    if layout_name == '3_03':
        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')
        clip3 = VideoFileClip(video03_filename, fps_source='fps')

        new_clip1 = clip1.resize((536, 1080))
        new_clip2 = clip2.resize((536, 1080))
        new_clip3 = clip3.resize((536, 1080))

        if delay01 > 0:
            black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
            new_clip1 = concatenate_videoclips([black_video01.resize((536, 1080)), clip1.resize((536, 1080))])
            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        if delay02 > 0:
            black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
            new_clip2 = concatenate_videoclips([black_video02.resize((536, 1080)), clip2.resize((536, 1080))])
            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        if delay03 > 0:
            black_video03 = black_video.subclip('00:00:00.000', milli_to_timecode(delay03))
            new_clip3 = concatenate_videoclips([black_video03.resize((536, 1080)), clip3.resize((536, 1080))])
            if volume03 != 1:
                new_clip3 = new_clip3.volumex(volume03)

        final_clip = CompositeVideoClip(
            [new_clip1.set_position((152, 0)), new_clip2.set_position((688, 0)),
             new_clip3.set_position((1224, 0))],
            size=(1920, 1080))

    if layout_name == '4_01':
        print(f'Start merge full video 4_01')

        clip1 = VideoFileClip(video01_filename, fps_source='fps')
        clip2 = VideoFileClip(video02_filename, fps_source='fps')
        clip3 = VideoFileClip(video03_filename, fps_source='fps')
        clip4 = VideoFileClip(video04_filename, fps_source='fps')

        new_clip1 = clip1.resize((960, 540))
        new_clip2 = clip2.resize((960, 540))
        new_clip3 = clip3.resize((960, 540))
        new_clip4 = clip4.resize((960, 540))

        if delay01 > 0:
            black_video01 = black_video.subclip('00:00:00.000', milli_to_timecode(delay01))
            new_clip1 = concatenate_videoclips([black_video01, clip1.resize((960, 540))])
            if volume01 != 1:
                new_clip1 = new_clip1.volumex(volume01)

        if delay02 > 0:
            black_video02 = black_video.subclip('00:00:00.000', milli_to_timecode(delay02))
            new_clip2 = concatenate_videoclips([black_video02, clip2.resize((960, 540))])
            if volume02 != 1:
                new_clip2 = new_clip2.volumex(volume02)

        if delay03 > 0:
            black_video03 = black_video.subclip('00:00:00.000', milli_to_timecode(delay03))
            new_clip3 = concatenate_videoclips([black_video03, clip3.resize((960, 540))])
            if volume03 != 1:
                new_clip3 = new_clip3.volumex(volume03)

        if delay04 > 0:
            black_video04 = black_video.subclip('00:00:00.000', milli_to_timecode(delay04))
            new_clip4 = concatenate_videoclips([black_video04, clip4.resize((960, 540))])
            if volume04 != 1:
                new_clip4 = new_clip4.volumex(volume04)

        final_clip = clips_array([[new_clip1.volumex(volume01), new_clip2.volumex(volume02)],
                                  [new_clip3.volumex(volume03), new_clip4.volumex(volume04)]])


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
        #final_clip2.subclipped(max(0, final_clip2.duration - 15), final_clip2.duration).write_videofile(final_filename)
        #final_clip2.write_videofile(final_filename)
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
    #merge_full('2_06', 'C:\\media\\mp4\\Jazz-03-Saxophone-P.mp4', 'C:\\media\\mp4\\Jazz-04-DoubleBass.mp4' , 0, 0, 1.0, 1.0, 'omiejung')
    merge_full('2_07', 'C:\\media\\mp4\\Jazz-04-DoubleBass.mp4', 'C:\\media\\mp4\\Jazz-03-Saxophone-P.mp4', '', '', 0, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 'omiejung')

    #merge_full('2_04', 'C:\\media\\mp4\\Jazz-02-Drum.mp4', 'C:\\media\\mp4\\Jazz-03-Saxophone.mp4',
    #           0, 2168,
    #           1.0, 1.0,
    #           'omiejung')
    #merge_full('2_04', 'C:\\media\\mp4\\Jazz-03-Saxophone.mp4', 'C:\\media\\mp4\\Jazz-02-Drum.mp4',
    #           2168, 0,
    #           1.0, 1.0,
    #           'omiejung')

    #merge_full('2_05', 'C:\\media\\mp4\\Jazz-03-Saxophone.mp4', 'C:\\media\\mp4\\Jazz-04-DoubleBass.mp4' , 0, 0, 1.0, 1.0, 'omiejung')

    #mix_sound('2_01', 'C:\\media\\mp4\\Jazz-03-Saxophone-P.mp4', 'C:\\media\\mp4\\Jazz-04-DoubleBass.mp4' , 0, 0, 1.0, 1.0, 'omiejung')
    print('Ad Astra Abyssosque')