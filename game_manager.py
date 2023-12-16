# 패키지
import tkinter as tk
import gc                               # 가비지 컬렉터
import os
from os.path import isfile, isdir       # 파일 유효성 검사 모듈
import platform, psutil, torch          # 기기 정보를 받아오는 모듈들
import random as r
import threading

# 커스텀 패키지
import player_class as pc
import inventory as inven

# 게임 매니저
class GameManager:

    # 키 인풋을 받을 변수
    keys = set()

    # tkinter 실행
    def __init__(self):
        root = tk.Tk()
        
        # title -> Kingslayer<season 1>: daybreaker V 0.0.1
        root.title(f"Kingslayer<{file.game_status_parse('season')}>: {file.game_status_parse('subtitle')}V {file.game_status_parse('version')}")
        root.geometry(f"{1}")
            
        root.bind("<KeyPress>", self.key_press_handler)
        root.bind("<KeyRelease>", self.key_release_handler)

        root.mainloop()

    # 눌렀을때
    def key_press_handler(self, e):
        self.keys.add(e.keycode)

    # 뗄때
    def key_release_handler(self, e):
        if e.keycode in self.keys:
            self.keys.remove(e.keycode)

    # 스킬 시전시 스레드화
    def Threading_suppoter(self, skill_func):
        skill_interrupt = threading.Thread()
        skill_interrupt.start()

    # 캔버스 정리 데코레이터
    def canvas_decorator(self, func, cvs):
        func()
        cvs.delete("all")

    def game_main_routine():
        # 타이틀
        while True:
            break

        # 로딩
        while True:
            player = Player_character_use_sword()
            break

        # 메인 게임 루틴 영역
        while True:
            if(len(self.keys)>0):
                if self.keys == 65 or self.keys == 97:
                    self.Threading_suppoter(player.A)



            root.update()

# 파일 매니저
class File_manager:
    def __init__(self):
        pass

    # 버그 레포트
    def BugReport(text):
        with open("BugReport_Log.txt", "w+") as file_name:
            # 파일을 처음 생성한 경우
            if file_name.read() == "":
                os_log = f'OS : {platform.system()}\nVersion : {platform.version()}\nArchitecture : {platform.architecture()}'
                graphic =  f'Graphic : {torch.cuda.get_device_name()}'
                cpu = f'CPU : {platform.processor()}'
                ram = f'RAM : {str(round(psutil.virtual_memory().total / (1024.0 ** 3)))+"GB"}'

                # 하드웨어 정보 찍어주기
                file_name.write(f'{os_log}\n{graphic}\n{cpu}\n{ram}\n')

            # 무조건 작성됨
            file_name.write(f'Log : \n{text}')

    def game_status_parse(params) -> str:
        try:
            with open('game_resource/GameStatus.txt', 'r', encoding='UTF-8') as gamestatus:
                lines = gamestatus.readlines()

                match params:
                    # 버전 가져와서 리턴
                    case 'version':
                        version_text = lines[0].strip().split(':')
                        return version_text[1]
                    case 'season':
                        season_text, season_number = lines[1].strip().split(':')
                        return f'{season_text} {season_number}'
                    case 'subtitle':
                        subtitle_text = lines[2].strip().split(':')
                        return subtitle_text[1]
                    case _:
                        raise Exception
                    
        except FileNotFoundError as FNFE:
            file.BugReport(f"GameStatus파일이 원래 경로에 존재하지 않습니다.")

        except Exception as EX:
            file.BugReport(f"문법상의 오류로 추정됨. 수정요망.")
            
    def awakeloading():
        pass

 # 시작
game = GameManager()
file = File_manager()
game.game_main_routine()