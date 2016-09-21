from cx_Freeze import setup, Executable


setup(
    name="Slither",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["sprites/snake_head.png",
                                             "sprites/red_apple.png",
                                             "sprites/red_apple_icon.ico"]}},
    description="Slither Game",
    executables=[Executable("main.py", icon="sprites/red_apple_icon.ico")]
)
