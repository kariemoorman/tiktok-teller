from downloaders.tiktok_downloader import TikTokVideoDownloader
from scrapers.tiktok_video_metadata_scraper import TiktokVideoMetadataScraper
from transcribers.tiktok_video_to_text import SpeechConverter
from nlp.keyword_extractor import extract_keywords
from nlp.emotion_extractor import filter_words
from cv.face_detection import FaceDetection

def main():
    print(
        '''


   __     __ __         __              __         
  |  \   |  \  \       |  \            |  \        
 _| ▓▓_   \▓▓ ▓▓   __ _| ▓▓_    ______ | ▓▓   __   
|   ▓▓ \ |  \ ▓▓  /  \   ▓▓ \  /      \| ▓▓  /  \  
 \▓▓▓▓▓▓ | ▓▓ ▓▓_/  ▓▓\▓▓▓▓▓▓ |  ▓▓▓▓▓▓\ ▓▓_/  ▓▓  
  | ▓▓ __| ▓▓ ▓▓   ▓▓  | ▓▓ __| ▓▓  | ▓▓ ▓▓   ▓▓   
  | ▓▓|  \ ▓▓ ▓▓▓▓▓▓\  | ▓▓|  \ ▓▓__/ ▓▓ ▓▓▓▓▓▓\   
   \▓▓  ▓▓ ▓▓ ▓▓  \▓▓\  \▓▓  ▓▓\▓▓    ▓▓ ▓▓  \▓▓\  
    \▓▓▓▓ \▓▓\▓▓   \▓▓   \▓▓▓▓  \▓▓▓▓▓▓ \▓▓   \▓▓  
                                                   
     __              __ __                   
    |  \            |  \  \                  
   _| ▓▓_    ______ | ▓▓ ▓▓ ______   ______  
  |   ▓▓ \  /      \| ▓▓ ▓▓/      \ /      \ 
   \▓▓▓▓▓▓ |  ▓▓▓▓▓▓\ ▓▓ ▓▓  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ 
    | ▓▓ __| ▓▓    ▓▓ ▓▓ ▓▓ ▓▓    ▓▓ ▓▓   \▓▓  
    | ▓▓|  \ ▓▓▓▓▓▓▓▓ ▓▓ ▓▓ ▓▓▓▓▓▓▓▓ ▓▓      
     \▓▓  ▓▓\▓▓     \ ▓▓ ▓▓\▓▓     \ ▓▓      
      \▓▓▓▓  \▓▓▓▓▓▓▓\▓▓\▓▓ \▓▓▓▓▓▓▓\▓▓      
    '''
    )
    
    print(
        '''
╔══════════════════════════════════════════════╗
║                                              ║
║    Choose from the options below:            ║
║                                              ║
║     [1] ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴛɪᴋᴛᴏᴋ ᴠɪᴅᴇᴏ              ║
║     [2] ᴛʀᴀɴsᴄʀɪʙᴇ ᴀ ᴛɪᴋᴛᴏᴋ ᴠɪᴅᴇᴏ            ║
║     [3] ᴀɴᴀʟʏᴢᴇ ᴀ ᴛɪᴋᴛᴏᴋ ᴠɪᴅᴇᴏ               ║
║     [exit] ᴏ̨ᴜɪᴛ ᴛʜᴇ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ              ║
║                                              ║
╚══════════════════════════════════════════════╝
        '''
    )
    
    while True:
        # Prompt the user for input
        user_input = input("Enter a command (1, 2, 3, or 'exit' to quit): ")

        # Check the user's input and perform tasks accordingly
        if user_input == '1':
            print("\nYou selected option 1.\n")
            url = input("Enter tiktok video URL: ")
            downloader = TikTokVideoDownloader([f'{url}'])
            downloader.download_tiktok_videos(browser='pyppeteer')

        elif user_input == '2':
            print("\nYou selected option 2. \n")
            mp4 = input("Enter mp4 filepath: ")
            speech_converter = SpeechConverter(f'{mp4}')
            speech_converter.extract_and_transform_speech()

        elif user_input == '3':
            print("\nYou selected option 3.\n")
            face_detection = input("Do you want face detection? (y/n): ")
            nlp = input("Do you want NLP? (y/n): ")
            if face_detection in ['y', 'yes', 'Y', 'YES', 'Yes']:
                mp4 = input("Enter mp4 filepath: ")
                output_directory = input("Enter output directory: ")
                detector = FaceDetection(mp4, output_directory)
                detector.detect_faces()
            else:
                pass
            if nlp in ['y', 'yes', 'Y', 'YES', 'Yes']:
                print('cool')
            else:
                pass                
            

        elif user_input.lower() == 'exit':
            print("\nExiting the program. Goodbye!\n")
            break 
        


if __name__ == "__main__":
    main()