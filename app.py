from video import make_video

def main():
    prompt = input("what video do you want to make? ")
    format = input("what format? ")
    make_video(format,prompt)




if __name__ == "__main__":
    main()