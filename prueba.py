try:
    import tkinter as tk
    from tkinter import messagebox, ttk, font, filedialog
    import openpyxl
    import time
    import requests
    import configparser
    import csv 
    from datetime import datetime
    import equisde
except ImportError as e:
    print(e)
    with open('errores.txt','w') as f:
        f.writelines(e)

else:
    print("Todo funciona :D")