import moviepy as mp
from moviepy import VideoFileClip



def print_hi(name):
    input_file = VideoFileClip("in05.mp4")
    output = mp.video.fx.Margin(10, color=(255, 255, 255)).add_margin(input_file)
    #output.apply()
    #final_clip = input_file.Margin(60)

    output.write_videofile("out05.mp4", fps=60)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
