import csv
import glob
import json
import os
import tkinter
import urllib
from datetime import timedelta, datetime
from tkinter import *
from tkinter import filedialog
import io
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

class Day_Simple(object):
    st_day = 0
    en_day = 0
    city_num = 0
    def __init__(self):
        self.day_simple = Tk()
        self.day_simple.title("기상종관 일자료 간소화")
        self.day_simple.geometry("600x400+400-500")
        self.day_simple.resizable(False, False)  # 크기 고정

        #메뉴바 생성
        menubar = tkinter.Menu(self.day_simple)

        menu_1 = tkinter.Menu(menubar, tearoff=0, activeborderwidth=2)
        menu_1.add_command(label="열기", command=self.file_open)
        menu_1.add_command(label="저장", command=self.file_save)
        menu_1.add_command(label="다른이름으로 저장", command=self.another_save)
        menu_1.add_command(label="인쇄")
        menu_1.add_command(label="내보내기")
        menu_1.add_separator()
        menu_1.add_command(label="닫기", command=self.close)
        menubar.add_cascade(label="파일", menu=menu_1)

        menu_2 = tkinter.Menu(menubar, tearoff=0, selectcolor="red", activeborderwidth=2)
        menu_2.add_radiobutton(label="API KEY", state="disable")
        menu_2.add_radiobutton(label="Tool")
        menu_2.add_radiobutton(label="GUI")
        menu_2.add_radiobutton(label="글꼴")
        menubar.add_cascade(label="설정", menu=menu_2)

        menu_3 = tkinter.Menu(menubar, tearoff=0, activeborderwidth=2)
        menu_3.add_checkbutton(label="기상자료 통계분석")
        menu_3.add_checkbutton(label="일반/특수 기상분석")
        menu_3.add_checkbutton(label="일별 자료")
        menubar.add_cascade(label="통계", menu=menu_3)

        menu_4 = tkinter.Menu(menubar, tearoff=0, activeborderwidth=2)
        menubar.add_cascade(label="정보", menu=menu_4)

        self.day_simple.config(menu=menubar)

        self.search_btn = tkinter.Button(self.day_simple, text = "검색", width = 15, height = 3,relief = "solid", bd=1, command = self.Weather_Day)
        self.search_btn.place(relx = 0.3, rely = 0.6)
        self.search_btn = tkinter.Button(self.day_simple, text="자료 통합", width=15, height=3, relief="solid", bd=1,command=self.sumfile)
        self.search_btn.place(relx=0.5, rely=0.6)

        self.label_start_day = tkinter.Label(self.day_simple, text = "시작일 : (YYYYMMDD)", width = 20)
        self.label_start_day.place(relx = 0.15, rely = 0.1)
        self.entry_start_day = tkinter.Entry(self.day_simple, width = 20)
        self.entry_start_day.place(relx = 0.4, rely = 0.1)
        self.label_end_day = tkinter.Label(self.day_simple, text="종료일 : (YYYYMMDD)", width=20)
        self.label_end_day.place(relx=0.15, rely=0.2)
        self.entry_end_day = tkinter.Entry(self.day_simple, width=20)
        self.entry_end_day.place(relx=0.4, rely=0.2)
        self.entry_city_search = tkinter.Entry(self.day_simple, width = 10, relief = "solid", bd=1, )
        self.entry_city_search.place(relx=0.4, rely=0.35)
        self.label_city_num = tkinter.Label(self.day_simple, text="지역 번호", width=20)
        self.label_city_num.place(relx=0.35, rely=0.28)
        self.label_city_num2 = tkinter.Label(self.day_simple, width=10)
        self.label_city_num2.place(relx=0.55, rely=0.35)


        self.values = [(90,"속초"),(93,"북춘천"),(95,"철원"),(98,"동두천"),(99,"파주"),(100,"대관령"),(101,"춘천"),
        (102,"백령도"),(104,"북강릉"),(105,"강릉"),(106,"동해"),(108,"서울"),(112,"인천"),(114,"원주"),(115,"울릉도"),(119,"수원"),
        (121,"영월"),(127,"충주"),(129,"서산"),(130,"울진"),(131,"청주"),(133,"대전"),(135,"추풍령"),(136,"안동"),(137,"상주"),
        (138,"포항"),(140,"군산"),(143,"대구"),(146,"전주"),(152,"울산"),(155,"창원"),(156,"광주"),(159,"부산"),(162,"통영"),
        (165,"목포"),(168,"여수"),(169,"흑산도"),(170,"완도"),(172,"고창"),(174,"순천"),(177,"홍성"),(184,"제주"),(185,"고산"),
        (188,"성산"),(189,"서귀포"),(192,"진주"),(201,"강화"),(202,"양평"),(203,"이천"),(211,"인제"),(212,"홍천"),(216,"태백"),
        (217,"정선군"),(221,"제천"),(226,"보은"),(232,"천안"),(235,"보령"),(236,"부여"),(238,"금산"),(239,"세종"),(243,"부안"),
        (244,"임실"),(245,"정읍"),(247,"남원"),(248,"장수"),(251,"고창군"),(252,"영광군"),(253,"김해시"),(254,"순창군"),
        (255,"북창원"),(257,"양산시"),(258,"보성군"),(259,"강진군"),(260,"장흥"),(261,"해남"),(262,"고흥"),(263,"의령군"),
        (264,"함양군"),(266,"광양시"),(268,"진도군"),(271,"봉화"),(272,"영주"),(273,"문경"),(276,"청송군"),(277,"영덕"),(278,"의성"),
        (279,"구미"),(281,"영천"),(283,"경주시"),(284,"거창"),(285,"합천"),(288,"밀양"),(289,"산청"),(294,"거제"),(295,"남해")]

        values1 = "전체", "수도권", "강원지방", "춘천", "청주", "대전","전주", "홍성", "안동", "광주", "청주", "목포", "창원", "대구", "제주", "인천"

        # 권역 콤보박스
        part_combo = ttk.Combobox(self.day_simple, width=5, height=5, values=values1)
        part_combo.place(rely=0.018, relx=0.01)
        part_combo.set("권역")
        # 지역 콤보박스
        self.part_combo2 = ttk.Combobox(self.day_simple, width=10, height=5, values=self.values)
        self.part_combo2.place(relx = 0.2, rely = 0.35)
        self.part_combo2.bind("<<ComboboxSelected>>", self.comboevent)
        self.part_combo2.current()
        self.part_combo2.set("지역")

        self.day_simple.mainloop()

    def comboevent(self, event):
        self.label_city_num2['text'] = self.part_combo2.get()
        self.label_city = self.label_city_num2['text']

    def close(self):  # close window
        from Start_Activity_GUI import Start_Activity
        self.day_simple.quit()
        self.day_simple.destroy()
        Start_Activity()

    def file_open(self):  # file open
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("Excel files", "*.xls"),
                                                         ("CSV_Excel", "*.csv"),
                                                         ("all files", "*.*",)))
        print(filename)

    def another_save(self):  # file another name save
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Excel files", "*.xls"),
                                                           ("CSV_Excel", "*.csv"),
                                                           ("all files", "*.*",)))
        print(filename)

    def file_save(self):  # file save
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Excel files", "*.xls"),
                                                           ("CSV_Excel", "*.csv"),
                                                           ("all files", "*.*",)))
        print(filename)

    def Weather_Day(self):
        Day_Simple.st_day = self.entry_start_day.get()
        Day_Simple.en_day = self.entry_end_day.get()
        Day_Simple.city_num = self.label_city
        print(Day_Simple.st_day, Day_Simple.en_day, Day_Simple.city_num)
        while True:
            st_day = str(Day_Simple.st_day)
            en_day = str(Day_Simple.en_day)
            city_num = str(Day_Simple.city_num)
            print(st_day, en_day, city_num)
            print("시작:" + st_day)
            print("종료:" + en_day)
            print("지역 :" + city_num)
            re_st_data = re.sub("-", "",st_day)
            re_en_data = re.sub("-", "",en_day)
            find_str = city_num.find(" ")
            find_num = city_num[:find_str]
            print("시작일re"+re_st_data)
            print("종료일re"+re_en_data)
            print("지역re:"+find_num)
            url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
            ufile = urllib.request.urlopen(url)
            content = ufile.read()
            nst_day = datetime.strptime(st_day, '%Y%m%d')
            nen_day = datetime.strptime(en_day, '%Y%m%d')
            to_day = nen_day - nst_day
            st_year = str(nst_day.year)
            mi_year = nen_day.year - nst_day.year
            dat_plus = nst_day + timedelta(days=1000)
            print(to_day)
            os.chdir(r"C:\Users\WM\Desktop\일자료 파일")
            numi = find_num
            nums = str(numi)
            if nen_day <= dat_plus: # start day ~ end day <= 1000day
                queryParams = '?' + \
                              'ServiceKey=' + 'your api key' + \
                              '&pageNo=' + '1' + \
                              '&numOfRows=' + '999' + \
                              '&dataType=' + 'JSON' + \
                              '&dataCd=' + 'ASOS' + \
                              '&dateCd=' + 'DAY' + \
                              '&startDt=' + st_day + \
                              '&endDt=' + en_day + \
                              '&stnIds=' + nums 

                result = requests.get(url + queryParams)
                js = json.loads(result.content)
                data = pd.DataFrame(js['response']['body']['items']['item'])

                data.drop(data.index[0])
                data.to_csv("일자료 지상종관" + st_year + ".csv", index=False)
                with open("일자료 지상종관" + st_year + ".csv", 'r', newline='', encoding='utf-8') as fi1:
                    with open("일자료_update" + st_year + ".csv", 'w', newline='') as fi2:
                        freader = csv.reader(fi1)
                        next(fi1)
                        fwriter = csv.writer(fi2)
                        header_list = ["지점번호", "지점", "날짜", "평균기온", "최저기온", "최저기온 시각", "최고기온", "최고기온 시각", "강수 계속시간",
                                       "10분 최다강수량", "10분 최다강수량 시각", "1시간 최다강수량", "1시간 최다 강수량 시각",
                                       "일강수량", "최대 순간풍속", "최대 순간 풍속풍향", "최대 순간풍속 시각", "최대 풍속", "최대 풍속 풍향",
                                       "최대 풍속 시각", "평균 풍속", "풍정합", "최다 풍향", "평균 이슬점온도", "최소 상대습도", "평균 상대습도 시각",
                                       "평균 상대습도", "평균 증기압", "평균 현지기압", "최고 해면 기압", "최고 해면기압 시각", "최저 해면기압",
                                       "최저 해면기압 시각", "평균 해면기압",
                                       "가조시간", "합계 일조 시간", "1시간 최다 일사 시각", "1시간 최다 일사량", "합계 일사량", "일 최심신적설",
                                       "일 최심신적설 시각", "일최심적설", "일 최심적설 시각", "합계 3시간 신적설", "평균 전운량", "평균 중하층운량",
                                       "평균 지면온도", "최저 초상온도", "평균 5cm 지중온도", "평균 10cm 지중온도", "평균 20cm 지중온도",
                                       "평균 30cm 지중온도", "0.5m 지중온도", "1.0m 지중온도", "1.5m 지중온도", "3.0m 지중온도",
                                       "5.0m 지중온도", "합계 대형증발량", "합계 소형증발량", "9-9강수", "일기현상", "안개 계속시간"]
                        fwriter.writerow(header_list)
                        for row in freader:
                            fwriter.writerow(row)
                test = input("O, X :")
                if test == "X" or "x":
                    break
            elif nen_day >= dat_plus: # start day ~ end day >= 1000day
                for i in range(mi_year + 1):
                    if i == 0:
                        st_day_1 = nst_day
                        en_day_1 = nst_day + relativedelta(months=11) + timedelta(days=30)
                        print(st_day_1, en_day_1)
                        st_year_1 = str(st_day_1.year)
                        st_d = str(datetime.strftime(st_day_1, '%Y%m%d'))
                        en_d = str(datetime.strftime(en_day_1, '%Y%m%d'))
                        queryParams = '?' + \
                                      'ServiceKey=' + 'your api key' + \
                                      '&pageNo=' + '1' + \
                                      '&numOfRows=' + '999' + \
                                      '&dataType=' + 'JSON' + \
                                      '&dataCd=' + 'ASOS' + \
                                      '&dateCd=' + 'DAY' + \
                                      '&startDt=' + st_d + \
                                      '&endDt=' + en_d + \
                                      '&stnIds=' + nums  

                        result = requests.get(url + queryParams)
                        js = json.loads(result.content)
                        data = pd.DataFrame(js['response']['body']['items']['item'])

                        data.drop(data.index[0])
                        data.to_csv("일자료 지상종관" + st_year_1 + ".csv", index=False)
                        with open("일자료 지상종관" + st_year_1 + ".csv", 'r', newline='', encoding='utf-8') as fi1:
                            with open("일자료_update" + st_year_1 + ".csv", 'w', newline='') as fi2:
                                freader = csv.reader(fi1)
                                next(fi1)
                                fwriter = csv.writer(fi2)
                                header_list = ["지점번호", "지점", "날짜", "평균기온", "최저기온", "최저기온 시각", "최고기온", "최고기온 시각",
                                               "강수 계속시간",
                                               "10분 최다강수량", "10분 최다강수량 시각", "1시간 최다강수량", "1시간 최다 강수량 시각",
                                               "일강수량", "최대 순간풍속", "최대 순간 풍속풍향", "최대 순간풍속 시각", "최대 풍속", "최대 풍속 풍향",
                                               "최대 풍속 시각", "평균 풍속", "풍정합", "최다 풍향", "평균 이슬점온도", "최소 상대습도", "평균 상대습도 시각",
                                               "평균 상대습도", "평균 증기압", "평균 현지기압", "최고 해면 기압", "최고 해면기압 시각", "최저 해면기압",
                                               "최저 해면기압 시각", "평균 해면기압",
                                               "가조시간", "합계 일조 시간", "1시간 최다 일사 시각", "1시간 최다 일사량", "합계 일사량", "일 최심신적설",
                                               "일 최심신적설 시각", "일최심적설", "일 최심적설 시각", "합계 3시간 신적설", "평균 전운량", "평균 중하층운량",
                                               "평균 지면온도", "최저 초상온도", "평균 5cm 지중온도", "평균 10cm 지중온도", "평균 20cm 지중온도",
                                               "평균 30cm 지중온도", "0.5m 지중온도", "1.0m 지중온도", "1.5m 지중온도", "3.0m 지중온도",
                                               "5.0m 지중온도", "합계 대형증발량", "합계 소형증발량", "9-9강수", "일기현상", "안개 계속시간"]
                                fwriter.writerow(header_list)
                                for row in freader:
                                    fwriter.writerow(row)
                    elif i != 0:
                        st_day_2 = nst_day + relativedelta(months=12 * i)
                        print(st_day_2)
                        st_year2 = str(st_day_2.year)
                        en_day_2 = nst_day + (relativedelta(months=12 * i) + relativedelta(months=11) + timedelta(days=30))
                        st_d2 = str(datetime.strftime(st_day_2, '%Y%m%d'))
                        en_d2 = str(datetime.strftime(en_day_2, '%Y%m%d'))
                        queryParams = '?' + \
                                      'ServiceKey=' + 'your api key' + \
                                      '&pageNo=' + '1' + \
                                      '&numOfRows=' + '999' + \
                                      '&dataType=' + 'JSON' + \
                                      '&dataCd=' + 'ASOS' + \
                                      '&dateCd=' + 'DAY' + \
                                      '&startDt=' + st_d2 + \
                                      '&endDt=' + en_d2 + \
                                      '&stnIds=' + nums 

                        result = requests.get(url + queryParams)
                        js = json.loads(result.content)
                        data = pd.DataFrame(js['response']['body']['items']['item'])

                        data.drop(data.index[0])
                        data.to_csv("일자료 지상종관" + st_year2 + ".csv", index=False)
                        with open("일자료 지상종관" + st_year2 + ".csv", 'r', newline='', encoding='utf-8') as fi1:
                            with open("일자료_update" + st_year2 + ".csv", 'w', newline='') as fi2:
                                freader = csv.reader(fi1)
                                next(fi1)
                                fwriter = csv.writer(fi2)
                                header_list = ["지점번호", "지점", "날짜", "평균기온", "최저기온", "최저기온 시각", "최고기온", "최고기온 시각",
                                               "강수 계속시간",
                                               "10분 최다강수량", "10분 최다강수량 시각", "1시간 최다강수량", "1시간 최다 강수량 시각",
                                               "일강수량", "최대 순간풍속", "최대 순간 풍속풍향", "최대 순간풍속 시각", "최대 풍속", "최대 풍속 풍향",
                                               "최대 풍속 시각", "평균 풍속", "풍정합", "최다 풍향", "평균 이슬점온도", "최소 상대습도", "평균 상대습도 시각",
                                               "평균 상대습도", "평균 증기압", "평균 현지기압", "최고 해면 기압", "최고 해면기압 시각", "최저 해면기압",
                                               "최저 해면기압 시각", "평균 해면기압",
                                               "가조시간", "합계 일조 시간", "1시간 최다 일사 시각", "1시간 최다 일사량", "합계 일사량", "일 최심신적설",
                                               "일 최심신적설 시각", "일최심적설", "일 최심적설 시각", "합계 3시간 신적설", "평균 전운량", "평균 중하층운량",
                                               "평균 지면온도", "최저 초상온도", "평균 5cm 지중온도", "평균 10cm 지중온도", "평균 20cm 지중온도",
                                               "평균 30cm 지중온도", "0.5m 지중온도", "1.0m 지중온도", "1.5m 지중온도", "3.0m 지중온도",
                                               "5.0m 지중온도", "합계 대형증발량", "합계 소형증발량", "9-9강수", "일기현상", "안개 계속시간"]
                                fwriter.writerow(header_list)
                                for row in freader:
                                    fwriter.writerow(row)
                test = input("O, X :")
                if test == "X" or "x":
                    break
            else:
                print("10년 단위로 입력")
                break

    def sumfile(self): # file sum
        input_path = r'Your directory path'  # search file path
        output_file = r'Your want filenaem.csv'  # result file name
        is_first_file = True
        for input_file in glob.glob(os.path.join(input_path, 'filename.csv')):  # search file name
            print(os.path.basename(input_file))
            with open(input_file, 'r', newline='') as csv_in_file:
                with open(output_file, 'a', newline='') as csv_out_file:
                    freader = csv.reader(csv_in_file)
                    fwriter = csv.writer(csv_out_file)
                    if is_first_file:
                        for row in freader:
                            fwriter.writerow(row)
                        is_first_file = False
                    else:
                        next(freader) #헤더를 건너뛰는 옵션
                        for row in freader:
                            fwriter.writerow(row)
                            break


