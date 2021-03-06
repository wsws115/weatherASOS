import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
from tkcalendar import *
import tkinter.font
from Day_simple_test import Day_simple_test


class Start_Activity:
    def __init__(self):
        self.st_app = Tk()
        self.st_app.geometry("800x600+300+100")
        self.st_app.title("API 추출 수집프로그램")
        self.st_app.resizable(False, False)  # 크기 고정
        self.st_app.configure(bg='#CCFFFF')
        font = tkinter.font.Font(family = "HY헤드라인M",size = 20)
        label_test1 = tkinter.Label(self.st_app, image=mark_image)
        label_test1.place(relx=0, rely=0.03, relwidth=1, relheight=0.2)
        label_title = tkinter.Label(self.st_app, text = "기상 수질자료 수집프로그램", font = font, bg = '#CCFFFF')
        label_title.place(relx = 0.17, rely = 0.27, width = 500, height = 30)

        weather_day_btn = tkinter.Button(self.st_app, text = "일 기상자료",relief = "solid", bd=2, font = font,bg = '#CCFFFF')
        weather_day_btn.place(relx= 0.37, rely = 0.4, width= 200, height = 40)

        weather_time_btn = tkinter.Button(self.st_app, text="시 기상자료",relief = "solid", bd=2, font=font,bg = '#CCFFFF')
        weather_time_btn.place(relx=0.37, rely=0.5, width=200, height=40)

        wather_btn = tkinter.Button(self.st_app, text="일자료 추출 간소화",relief = "solid", bd=2, font=font,bg = '#CCFFFF', command=self.day_simple_btn)
        wather_btn.place(relx=0.31, rely=0.6, width=300, height=40)

        wather_btn = tkinter.Button(self.st_app, text="수자원정보", relief="solid", bd=2, font=font, bg='#CCFFFF',
                                    command=self.water_re_btn)
        wather_btn.place(relx=0.37, rely=0.7, width=200, height=40)

        statistics_btn = tkinter.Button(self.st_app, text="통계",relief = "solid", bd=2, font=font,bg = '#CCFFFF')
        statistics_btn.place(relx=0.37, rely=0.8, width=200, height=40)

        self.st_app.mainloop()

    def day_simple_btn(self):
        print("일자료 간소화")
        self.st_app.quit()
        self.st_app.destroy()
        Day_Simple()    

if __name__ == '__main__':
    Example1 = Start_Activity()
