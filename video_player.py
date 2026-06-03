def start_video(page):

    page.evaluate("""
    () => {
        const video = document.querySelector('video');

        if(video){
            video.play();
        }
    }
    """)


def get_video_duration(page):

    return page.evaluate("""
    () => {
        const video = document.querySelector('video');

        return video ? video.duration : 0;
    }
    """)
