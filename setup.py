from cx_Freeze import setup, Executable

setup(
    name="polycrack",
    version="1.0",
    description="Brute force la adresa stuenti.pub.ro",
    executables=[Executable("polycrack.py")]
)