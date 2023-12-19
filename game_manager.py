# © 2023. neutronflare1 all rights reserved.

# 패키지
import tkinter as tk
import tkinter.messagebox as echo
import gc  # 가비지 컬렉터
import os
from os.path import isfile, isdir  # 파일 유효성 검사 모듈
import platform, psutil, torch  # 기기 정보를 받아오는 모듈들
import random as r
import threading

# 커스텀 패키지
import player_class as pc
import inventory as inven
import boss_class as bc


# 게임 매니저
class GameManager:
    # 키 인풋을 받을 변수
    keys = set()

    # tkinter 실행
    def __init__(self, root):
        # 해상도에 따른 화면 좌표값(모든 UI의 비율을 잡는데 사용)
        self.resolution_center = file.game_setting_parse("resolution")
        self.resolution_xscale = file.game_setting_parse("resolution_x")
        self.resolution_yscale = file.game_setting_parse("resolution_y")

        self.root = root

        # title -> Kingslayer <season 1> : daybreaker V 0.0.1
        self.root.title(
            f"Kingslayer <{file.game_status_parse('season')}> : {file.game_status_parse('subtitle')} V {file.game_status_parse('version')}"
        )
        self.root.geometry(self.resolution_center)
        self.root.resizable(False, False)

        self.cvs = tk.Canvas(
            self.root,
            width=self.resolution_xscale,
            height=self.resolution_yscale,
            bg="black",
        )
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

    # 화면 옮겨다니기
    def control_suppoter(self, frame_status):
        match frame_status:
            case 0:
                graphic.title(frame_status)

            case 1:
                graphic.loading(frame_status)

            case 2:
                graphic.ingame(frame_status)

            case _:
                raise Exception("status parameter 값에 문제가 있습니다.")

    # 게임 메인
    def game_main_routine(self):
        global frame_status, frame_swap_boolean
        frame_status = 0
        frame_swap_boolean = True

        # 시작 전 추가 작업
        self.bind_suppoter()
        try:
            # image 매핑
            player_character = tk.PhotoImage(
                file=file.path + "\game_resource\makeshift_player_sprite.png"
            )
            boss = tk.PhotoImage(
                file=file.path + "\game_resource\enemy_character_sprite.png"
            )
            bg = tk.PhotoImage(
                file=file.path + "\game_resource\isback_ground_image.png"
            )

        except FileNotFoundError as FNFE:
            file.bugreport(f"존재하지 않는 파일이 있습니다.")

        # 인게임 무한루프
        while True:
            if frame_swap_boolean == True:
                self.control_suppoter(frame_status)
                frame_swap_boolean == False

            self.root.update()


class GraphicManager:
    # 인벤토리 호출
    def inventory_call():
        pass

    # 프레임 스왑 도우미
    def frame_swap_supporter(self, param):
        global frame_status, frame_swap_boolean
        frame_status = param
        frame_swap_boolean = True

    # 타이틀
    def title(self):
        # 캔버스 정리
        def title_canvas_clear():
            self.frame_swap_supporter(1)

            game.cvs.delete("title_text")
            start_button.pack_forget()
            inventory_button.pack_forget()
            gc.collect()

        game.cvs.create_text(
            game.root,
            (game.resolution_xscale % 2),
            ((game.resolution_yscale % 2) - (game.resolution_yscale % 6)),
            text="KingSlayer",
            fill="DeepSkyBlue2",
            font=("Times New Roman", 36),
            tags="title_text",
        )
        start_button = tk.Button(game.root, text="시작", command=title_canvas_clear)
        start_button.place(
            x=(game.resolution_xscale % 2),
            y=((game.resolution_yscale % 2) + (game.resolution_yscale % 12)),
        )
        inventory_button = tk.Button(game.root, text="시작", command=next)
        inventory_button.pack()

    # 로딩창
    def loading(self):
        pass

    def ingame():
        pass


# 파일 매니저
class FileManager:
    # 현재 스크립트 파일 절대경로 확보 -> 기준점
    path = os.path.dirname(os.path.abspath(__file__))

    # 버그 레포트
    def bugreport(self, text: str):
        with open("BugReport_Log.txt", "w+", encoding="UTF-8") as file_name:
            # 파일을 처음 생성한 경우
            if file_name.read() == "":
                os_log = f"OS : {platform.system()}\nVersion : {platform.version()}\nArchitecture : {platform.architecture()}"
                graphic = f"Graphic : {torch.cuda.get_device_name()}"
                cpu = f"CPU : {platform.processor()}"
                ram = f'RAM : {str(round(psutil.virtual_memory().total / (1024.0 ** 3)))+"GB"}'

                # 하드웨어 정보 찍어주기
                file_name.write(f"{os_log}\n{graphic}\n{cpu}\n{ram}\n")

            # 무조건 작성됨
            file_name.write(f"Log : \n{text}")

    # 게임 스테이터스애서 데이터를 가져옴
    def game_status_parse(self, params) -> str:
        try:
            with open(
                self.path + "\game_resource\GameStatus.txt", "r", encoding="UTF-8"
            ) as gamestatus:
                lines = gamestatus.readlines()

                match params:
                    # 버전 가져와서 리턴
                    case "version":
                        version_text = lines[2].strip().split(":")
                        return version_text[1].replace('"', "")
                    case "season":
                        season_text, season_number = lines[3].strip().split(":")
                        return f"{season_text} {season_number}".replace('"', "")
                    case "subtitle":
                        subtitle_text = lines[4].strip().split(":")
                        return subtitle_text[1].replace('"', "")
                    case _:
                        raise Exception

        except FileNotFoundError as FNFE:
            file.bugreport(f"GameStatus 파일이 원래 경로에 존재하지 않습니다.")
            issue_exit_suppoter()

        except Exception as EX:
            file.bugreport(f"gamestatus file issue")
            issue_exit_suppoter()

    # 게임 설정값 가져옴
    def game_setting_parse(self, params) -> str or int:
        try:
            with open(
                self.path + "\game_resource\Settings.txt", "r", encoding="UTF-8"
            ) as gamesetting:
                lines = gamesetting.readlines()

                match params:
                    # 세팅값 가져와서 리턴
                    case "resolution":
                        resolution = lines[3].strip().split(":")
                        return resolution[1].replace('"', "")
                    case "resolution_x":
                        resolution = lines[3].strip().split(":")
                        xscale = resolution[1].strip().split("x")
                        return xscale[0].replace('"', "")
                    case "resolution_y":
                        resolution = lines[3].strip().split(":")
                        yscale = resolution[1].strip().split("x")
                        return yscale[1].replace('"', "")
                    case _:
                        raise Exception

        except FileNotFoundError as FNFE:
            file.bugreport(f"Settings 파일이 원래 경로에 존재하지 않습니다.")
            issue_exit_suppoter()

        except Exception as EX:
            file.bugreport(f"gamesetting file issue")
            issue_exit_suppoter()


class SettingManager:
    pass


class SoundManager:
    pass


# 일반적인 겜 종료
def normal_exit_suppoter(response):
    if response == 1:
        root.destroy()
        root.quit()
        exit()
    elif response == 0:
        return


# 이슈로 인한 겜 종료
def issue_exit_suppoter():
    root.destroy()
    root.quit()
    exit()


# 시작
root = tk.Tk()

file = FileManager()
setting = SettingManager()
sound = SoundManager()
graphic = GraphicManager()
game = GameManager(root)

game.game_main_routine()
