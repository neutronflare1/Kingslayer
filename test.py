# import tkinter
# import random

# def resize():
#     a = random.randrange(1000, 1600)
#     b = random.randrange(300, 900)
#     root.geometry(f"{a}x{b}")

# root = tkinter.Tk()
# root.geometry("1600x900")
# root.resizable(False, False)

# btn = tkinter.Button(root, text="누를시?", width = 5, height = 2, command=resize)
# btn.pack()

# root.mainloop()

# with open('./project_folder/game_resource/GameStatus.txt', 'r', encoding='UTF-8') as f:
#     lines = f.readline()
#     e = lines.strip().split(':')
#     print(f'{e[0]}:{e[1]}')

# for i in StatusFileLine:
#     print(StatusFileLine["version"])

# def game_version_parse():
#     with open('./GameStatus.txt', 'r') as version:
#         game_version = version.readlines()