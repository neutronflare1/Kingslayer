# © 2023. neutronflare1 all rights reserved.

# 패키지
import tkinter as tk
import tkinter.messagebox as echo
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
        self.root = tk.Tk()
        
        # title -> Kingslayer<season 1>: daybreaker V 0.0.1
        self.root.title(f"Kingslayer<{file.game_status_parse('season')}>: {file.game_status_parse('subtitle')}V {file.game_status_parse('version')}")
        self.root.geometry(f"{file.game_setting_parse('resolution')}")
        self.root.resizable(False, False)

        self.cvs = tk.Canvas(self.root, width = 100, height = 100, bg = "black")
        self.cvs.pack(fill="both", expand=True)

        self.root.mainloop()

    # 눌렀을때
    def key_press_handler(self, e):
        self.keys.add(e.keycode)

    # 뗄때
    def key_release_handler(self, e):
        if e.keycode in self.keys:
            self.keys.remove(e.keycode)

    # init에서 bind하지 못하는 문제점 해결용 메서드 분리
    def bind_suppoter(self):
        self.root.bind("<KeyPress>", self.key_press_handler)
        self.root.bind("<KeyRelease>", self.key_release_handler)

    # 일반적인 겜 종료
    def normal_exit_suppoter(self, response):
        if response==1:
            self.root.destroy()
            self.root.quit()
            exit()
        elif response == 0:
            return

    # 이슈로 인한 겜 종료
    def issue_exit_suppoter(self):
        self.root.destroy()
        self.root.quit()
        exit()

    # 스킬 시전시 스레드화
    def threading_suppoter(self, skill_func):
        skill_interrupt = threading.Thread()
        skill_interrupt.start()

    # 게임 메인
    def game_main_routine(self):
        status = 0

        # 시작 전 추가 작업
        self.bind_suppoter()
        file.awake_suppoter()

        # 타이틀
        while True:
            match status:
                case 0:
                    graphic.title()

        # 로딩
        while True:
            
            break

        # 메인 게임 루틴 영역
        while True:
            if(len(self.keys)>0):
                if self.keys == 65 or self.keys == 97:
                    self.threading_suppoter()



            self.root.update()

class GraphicManager:
    # 캔버스 정리 데코레이터
    def canvas_decorator(self, func, target:str):
        def wrapper():
            game.cvs.delete(target)
            func()          
        return wrapper
    
    @canvas_decorator
    def title(self):
        game.cvs.create_rectangle()


# 파일 매니저
class FileManager:
    
    # 버그 레포트
    def bugreport(text):
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
                        version_text = lines[3].strip().split(':')
                        return version_text[1]
                    case 'season':
                        season_text, season_number = lines[4].strip().split(':')
                        return f'{season_text} {season_number}'
                    case 'subtitle':
                        subtitle_text = lines[5].strip().split(':')
                        return subtitle_text[1]
                    case _:
                        raise Exception
                    
        except FileNotFoundError as FNFE:
            file.bugreport(f"GameStatus 파일이 원래 경로에 존재하지 않습니다.")
            file.exit_suppoter()

        except Exception as EX:
            file.bugreport(f"gamestatus file issue")
            file.exit_suppoter()

    def game_setting_parse(params) -> str or int:
        try:
            with open('game_resource/Settings.txt', 'r', encoding='UTF-8') as gamesetting:
                lines = gamesetting.readlines()

                match params:
                    # 세팅값 가져와서 리턴
                    case 'resolution':
                        resolution = lines[4].strip().split(':')
                        return resolution[1]
                    case _:
                        raise Exception
                    
        except FileNotFoundError as FNFE:
            file.bugreport(f"Settings 파일이 원래 경로에 존재하지 않습니다.")

        except Exception as EX:
            file.bugreport(f"gamesetting file issue")
            
    # 원래 만들었던 레거시의 코드구조에서 터치하지 않은 상태
    def awake_suppoter():
        try:
            # 파일의 존재 여부 검사
            player_character = tk.PhotoImage(file = "./game_resource/main_character_sprite.png")
            boss = tk.PhotoImage(file = './game_resource/enemy_character_sprite.png')
            bg = tk.PhotoImage(file = "./game_resource/backgroundimage.png")
            floor = tk.PhotoImage(file = "./game_resource/floorimage.png")    

        except FileNotFoundError as FNFE:
            file.bugreport(f"존재하지 않는 파일이 있습니다.")

        except:
            pass

        else:
            # 정상적으로 준비된 파일들 객체화
            
            return player_character, boss, bg, floor

class SettingManager:
    pass

class SoundManager:
    pass

# 시작
file = FileManager()
setting = SettingManager()
sound = SoundManager()
graphic = GraphicManager()
game = GameManager()
game.game_main_routine()