import os
import openai
import argparse
import os
import utils
import requests
import os
import json
import pyaudio
import wave
import time
import sys
from urllib.request import urlopen
from time import sleep
from pydub import AudioSegment
import tkinter
import customtkinter
from PIL import Image
import tkinter.messagebox
from PIL import ImageTk, Image

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

openai.api_key = "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"
API_KEY = "077ee4131c2b4d3dbd6f5fafaefd3fc0"
UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'
AUDIO_FILE = 'audio.mp3'
TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'
OUTPUT_TRANSCRIPT_FILE = 'speech-to-text-tutorial.txt'

dir = os.path.join(r"C:\Users\Admin\Desktop\Ai")
if not os.path.exists(dir):
    os.mkdir(dir)

def getsound():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels= CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer= CHUNK
                    )
    print("Start recording...")

    frames=[]
    seconds = 3
    for i in range(0, int(RATE/ CHUNK * seconds)):
        data=stream.read(CHUNK)
        frames.append(data)

    print("recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("output.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()







def read_audio_file(file):
  """Helper method that reads in audio files"""
  with open(file, 'rb') as f:
    while True:
      data = f.read(5242880)
      if not data:
        break
      yield data


def audiototext():
    headers = {
        'authorization': "077ee4131c2b4d3dbd6f5fafaefd3fc0",
        'content-type': 'application/json'
    }

    res_upload = requests.post(
     UPLOAD_ENDPOINT,
     headers=headers,
     data=read_audio_file(AUDIO_FILE)
             )
    upload_url = res_upload.json()['upload_url']
    res_transcript = requests.post(
     TRANSCRIPT_ENDPOINT,
     headers=headers,
     json={
        'audio_url': upload_url,
        'iab_categories': True,
         },
     )
    res_transcript_json = res_transcript.json()
    print("Started audio to text")
    status = ''
    while status != 'completed':
        res_result = requests.get(
        TRANSCRIPT_ENDPOINT + "/" + res_transcript_json['id'],
        headers=headers
        )
        print(TRANSCRIPT_ENDPOINT + "/" + res_transcript_json['id'])
    status = res_result.json()['status']
    print(f'Status: {status}')
    if status == 'error':
        sys.exit('Audio file failed to process.')
        print('Audio file failed to process.')
    elif status != 'completed':
            sleep(100)
            print(res_result.json()['text'])
    with open(OUTPUT_TRANSCRIPT_FILE, 'w') as f:
            f.write(res_result.json()['text'])
            print(f'Transcript file saved under {OUTPUT_TRANSCRIPT_FILE}')



#getsound();
#audiototext();
#createAd()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Post With AI")
        self.geometry("900x500")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path,
                                                                         "test/manual_integration_tests/test_images/CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path,
                                                                               "test/manual_integration_tests/test_images/large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path,
                                                                               "test/manual_integration_tests/test_images/image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path,
                                                                                     "test/manual_integration_tests/test_images/home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path,
                                                                                    "test/manual_integration_tests/test_images/home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path,
                                                                                     "test/manual_integration_tests/test_images/chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path,
                                                                                    "test/manual_integration_tests/test_images/chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path,
                                                                                         "test/manual_integration_tests/test_images/add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path,
                                                                                        "test/manual_integration_tests/test_images/add_user_light.png")), size=(20, 20))

        self.language_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/language.png")),
            dark_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/language.png")), size=(20, 20))
        self.user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/user.png")),
            dark_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/user.png")), size=(20, 20))
        self.customer_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/customer.png")),
            dark_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/customer.png")),
            size=(20, 20))
        self.summary_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/summary.png")),
            dark_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/summary.png")),
            size=(20, 20))
        self.simple_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/simple.png")),
            dark_image=Image.open(os.path.join(image_path, "test/manual_integration_tests/test_images/simple.png")),
            size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Create with AI", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Create Advert",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Advert Pic",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Product Name",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.user_image, anchor="w",
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Change text Language",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.language_image, anchor="w",
                                                      command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Notes to Summary",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.summary_image, anchor="w",
                                                      command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        self.frame_7_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Customer interview Questions",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.customer_image, anchor="w",
                                                      command=self.frame_7_button_event)
        self.frame_7_button.grid(row=7, column=0, sticky="ew")

        self.frame_8_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Simplify",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.simple_image, anchor="w",
                                                      command=self.frame_8_button_event)
        self.frame_8_button.grid(row=8, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0",
                            "Welcome to Post with Ai\n\n" + "This platform allows users to leverage the power of ai to come up with ideas for ads ,"
                                                            " products, content etc. We are working on more features,"
                                                            
                                                            
                                               "\n\n Features \n\n"
                            "Create Advert\n"
                            'Turn a product description into ad copy. Just write the product description well and get your ad content'
                                                            
                                                            "\n\nAdvert Pic\n"
                                                            'Creating images from scratch based on a text prompt. Let the ai generate pis for your next ad campaign that are original and unique just give it a good and clear description of what you want'
                                                            "\n\nProduct Name\n"
                                                            'Create product names from examples words. Influenced by a community prompt. '
                                                            'Product description: A home milkshake maker'
                                                            'Seed words: fast, healthy, compact'
                            "Product names: HomeShaker, Fit Shaker, QuickShake, Shake Maker"
                                                            "Product description: A pair of shoes that can fit any foot size."
                            "Output = Product names: AdaptFit, OmniSecure, Fit-All, AdaptShoes."
                                                            "\n\nChange text language\n"
                                                            'Translates English text into French, Spanish and Japanese.'
                                                            "\n\nNotes to Summary\n"
                                                            'Turn meeting notes into a summary.\n Convert my short hand into a first-hand account of the meeting:'
                                                            
                                                            "\n\nCustomer interview questions\n"
                                                            'Create interview questions.'
                                                            "\n\nSimplify\n"
                                                            'Translates difficult text into simpler concepts..'
                            )
        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Analysis" ,command= self.createAd)
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.second_frame_entry_1 = customtkinter.CTkEntry(self.second_frame, placeholder_text="Write a creative ad for the following product to run on Facebook aimed at parents:\n.....", width=480, height=80)
        self.second_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.second_frame_label_1 = customtkinter.CTkLabel(self.second_frame, text="Ad Text")
        self.second_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20),sticky="nsew")
        self.textbox2 = customtkinter.CTkEntry(self.second_frame, placeholder_text="Please wait",
                                              width=480, height=80,
                                               )
        self.textbox2.grid(row=4, column=0, padx=(20, 0), pady=(20, 20))


        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="Generate", command=self.createPic)
        self.third_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.third_frame_button_2 = customtkinter.CTkButton(self.third_frame, text="Generate from Image", command=self.createPic)
        self.third_frame_button_2.grid(row=1, column=1, padx=20, pady=10)
        self.third_frame_entry_1 = customtkinter.CTkEntry(self.third_frame, placeholder_text="Enter description",
                                                           width=480, height=80)
        self.third_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.third_frame_label_1 = customtkinter.CTkLabel(self.third_frame, text="Ad Pic")
        self.third_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.ad_image = ImageTk.PhotoImage(Image.open(os.path.join(image_path,
                                                                   "test/manual_integration_tests/test_images/user.png"))
                       ,size=(200, 150))
        self.image_label = customtkinter.CTkLabel(self.third_frame, image=self.ad_image).grid(row = 4)
        self.textboxc = customtkinter.CTkEntry(self.third_frame, placeholder_text="Please wait",
                                               width=480, height=80,
                                               )
        self.textboxc.grid(row=5, column=0, padx=(20, 0), pady=(20, 20))
        self.ad_image2 = ImageTk.PhotoImage(Image.open(os.path.join(image_path,
                                                                   "test/manual_integration_tests/test_images/user.png"))
                                           , size=(200, 150))
        self.image_label2 = customtkinter.CTkLabel(self.third_frame, image=self.ad_image).grid(row=6,  padx=(20, 0), pady=(20, 20),)

        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame_button_1 = customtkinter.CTkButton(self.fourth_frame, text="Analysis", command=self.ProductName)
        self.fourth_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.fourth_frame_entry_1 = customtkinter.CTkEntry(self.fourth_frame, placeholder_text="Product description:\n.......",
                                                           width=480, height=80)
        self.fourth_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.fourth_frame_label_1 = customtkinter.CTkLabel(self.fourth_frame, text="Product Name")
        self.fourth_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox4 = customtkinter.CTkEntry(self.fourth_frame, placeholder_text="Please wait",
                                              width=480, height=80,
                                              )
        self.textbox4.grid(row=4, column=0, padx=(20, 0), pady=(20, 20))

        # create five frame
        self.five_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.five_frame_button_1 = customtkinter.CTkButton(self.five_frame, text="Analysis", command=self.translation)
        self.five_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.five_frame_entry_1 = customtkinter.CTkEntry(self.five_frame, placeholder_text="Translate this into 1. French, 2. Spanish and 3. Japanese:\n.......",
                                                           width=480, height=80)
        self.five_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.five_frame_label_1 = customtkinter.CTkLabel(self.five_frame, text="Translation")
        self.five_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox5 = customtkinter.CTkEntry(self.five_frame , placeholder_text="Please wait",
                                              width=480, height=80,
                                              )
        self.textbox5.grid(row=4, column=0, padx=(20, 0), pady=(20, 20))

        # create Six frame
        self.six_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.six_frame_button_1 = customtkinter.CTkButton(self.six_frame, text="Analysis", command=self.notestoSmmary)
        self.six_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.six_frame_entry_1 = customtkinter.CTkEntry(self.six_frame, placeholder_text="Turn meeting notes into a summary:\n .......",
                                                         width=480, height=80)
        self.six_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.six_frame_label_1 = customtkinter.CTkLabel(self.six_frame, text="Summary generated")
        self.six_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox6 = customtkinter.CTkEntry(self.six_frame, placeholder_text="Please wait",
                                              width=480, height=80,
                                              )
        self.textbox6.grid(row=4, column=0, padx=(20, 0), pady=(20, 20))

        # create Seven frame
        self.seven_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.seven_frame_button_1 = customtkinter.CTkButton(self.seven_frame, text="Analysis", command=self.interviewQuestions)
        self.seven_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.seven_frame_entry_1 = customtkinter.CTkEntry(self.seven_frame, placeholder_text="Create a list of 8 questions for my interview with a science fiction author:\n.....",
                                                        width=480, height=80)
        self.seven_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.seven_frame_label_1 = customtkinter.CTkLabel(self.seven_frame, text="Questions Generated")
        self.seven_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox7 = customtkinter.CTkEntry(self.seven_frame, placeholder_text="Please wait",
                                              width=480, height=80,
                                              )
        self.textbox7.grid(row=4, column=0, padx=(20, 0), pady=(20, 20))

        # create Eight frame
        self.eight_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.eight_frame_button_1 = customtkinter.CTkButton(self.eight_frame, text="Analysis", command=self.simple)
        self.eight_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.eight_frame_button_2 = customtkinter.CTkButton(self.eight_frame, text="Get Keywords", command=self.keywords)
        self.eight_frame_button_2.grid(row=1, column=1, padx=20, pady=10)
        self.eight_frame_entry_1 = customtkinter.CTkEntry(self.eight_frame, placeholder_text="Extract keywords from this text:\n .......\nSummarize this for a second-grade student:\n.....",
                                                          width=480, height=80)
        self.eight_frame_entry_1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20))
        self.eight_frame_label_1 = customtkinter.CTkLabel(self.eight_frame, text="Simplified text")
        self.eight_frame_label_1.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox8 = customtkinter.CTkEntry(self.eight_frame, placeholder_text="Please wait",
                                              width=480, height=80,
                                              )
        self.textbox8.grid(row=4, column=0, padx=(20, 0), pady=(20, 20))
        self.eight_frame_label_2 = customtkinter.CTkLabel(self.eight_frame, text="Keywords")
        self.eight_frame_label_2.grid(row=5, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox9 = customtkinter.CTkEntry(self.eight_frame, placeholder_text="Please wait",
                                                width=480, height=80,
                                                )
        self.textbox9.grid(row=6, column=0, padx=(20, 0), pady=(20, 20))
        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "Create Advert" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "Advert Pic" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Create Advert":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "Advert Pic":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "Product Name":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "Change text language":
            self.five_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.five_frame.grid_forget()
        if name == "Notes to Summary":
            self.six_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.six_frame.grid_forget()
        if name == "Customer interview Questions":
            self.seven_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.seven_frame.grid_forget()
        if name == "Simplify":
            self.eight_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.eight_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("Create Advert")

    def frame_3_button_event(self):
        self.select_frame_by_name("Advert Pic")

    def frame_4_button_event(self):
        self.select_frame_by_name("Product Name")
    def frame_5_button_event(self):
        self.select_frame_by_name("Change text language")

    def frame_6_button_event(self):
        self.select_frame_by_name("Notes to Summary")

    def frame_7_button_event(self):
        self.select_frame_by_name("Customer interview Questions")
    def frame_8_button_event(self):
        self.select_frame_by_name("Simplify")
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def createAd(self):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= self.second_frame_entry_1.get(),
            temperature=0.5,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response.choices[0].text)


        self.textbox2.insert("0", response.choices[0].text)



    def createPic(self):
      response = openai.Image.create(
          prompt= self.third_frame_entry_1.get(),
          n=1,
          size='256x256'
      )
      image_url = response['data'][0]['url']
      u = urlopen(image_url)
      raw_data = u.read()
      u.close()
      print(image_url)

      self.ad_image = ImageTk.PhotoImage(
          data = raw_data,
          size=(500, 150))
      self.image_label = customtkinter.CTkLabel(self.third_frame, image=self.ad_image).grid(row=4)
      self.textboxc.insert("0", image_url)

    def createPicfromPic(self):
      response = openai.Image.create(
          image=open(r"C:\Users\Admin\Desktop\Ai\input.jpg", "rb"),
          prompt= self.third_frame_entry_1.get(),
          n=1,
          size='256x256'
      )
      image_url = response['data'][0]['url']
      u = urlopen(image_url)
      raw_data = u.read()
      u.close()
      print(image_url)

      self.ad_image = ImageTk.PhotoImage(
          data = raw_data,
          size=(500, 150))
      self.image_label = customtkinter.CTkLabel(self.third_frame, image=self.ad_image).grid(row=4)

    def notestoSmmary(self):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= self.six_frame_entry_1.get(),
            temperature=0,
            max_tokens=64,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response.choices[0].text)

        self.textbox6.insert("0", response.choices[0].text)

    def interviewQuestions(self):

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= self.seven_frame_entry_1.get(),
            temperature=0.5,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response.choices[0].text)

        self.textbox7.insert("0", response.choices[0].text)

    def ProductName(self):

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= self.fourth_frame_entry_1.get(),
            temperature=0.8,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response.choices[0].text)

        self.textbox4.insert("0", response.choices[0].text)

    def translation(self):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.five_frame_entry_1.get(),
                temperature=0.8,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response.choices[0].text)

            self.textbox5.insert("0", response.choices[0].text)

    def simple(self):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.eight_frame_entry_1.get(),
                temperature=0.8,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response.choices[0].text)

            self.textbox8.insert("0", response.choices[0].text)

    def keywords(self):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= self.eight_frame_entry_1.get(),
                temperature=0.5,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.8,
                presence_penalty=0.0
            )
            self.textbox9.insert("0", response.choices[0].text)





if __name__ == "__main__":
    app = App()
    app.mainloop()