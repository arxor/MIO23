#
# COM SETTINGS
#
COM_BAUD = 57600
COM_TIMEOUT = 0.05
#
# BRACELET SETTINGS
#
NUM_CHANNELS = 9
NUM_SIGNALS = 11
CHANNELS = ["abp1", "abp2", "ref", "ax", "ay", "az", "gx", "gy", "gz", "ft1", "ft2"]
BUFFERS_LEN = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 50, 50]
NORMALIZE_MIN = [0, 0, 0, -4096, -4096, -4096, -16384, -16384, -16384]
NORMALIZE_MAX = [1023, 1023, 1023, 4095, 4095, 4095, 16383, 16383, 16383]
# OPTINON MENUS
OPTIONMENU_COM_CHOOSE = "Выберите порт"
OPTIONMENU_NO_COM = "Нет доступных портов"

# BUTTONS
BUTTON_CONNECT = "Подключиться"

# WINDOW TITLE
WINDOW_TITLE = "Электромиографический браслет"

# WINDOW SIZE = screen_size / WINDOWSIZE_DIVIDER
WINDOWSIZE_DIVIDER = 1.2

#
# PLOT SETTINGS
#

# PLOT TITLES
PLOTTITLE_1 = 'Сгибатели'
PLOTTITLE_2 = 'Разгибатели'
PLOTTITLE_3 = 'Опорное напряжение'
PLOTTITLE_4 = 'Ускорение x'
PLOTTITLE_5 = 'Ускорение y'
PLOTTITLE_6 = 'Ускорение z'
PLOTTITLE_7 = 'Угловая скорость x'
PLOTTITLE_8 = 'Угловая скорость y'
PLOTTITLE_9 = 'Угловая скорость z'

# PLOT AUTOSCALE
PLOT_AUTOSCALE = 50

# PLOT FONT
PLOT_FONTSIZE = 7

# PLOT SIZE
PLOT_FIGSIZE = tuple(map(lambda x: x / 1.3, (3, 1.8)))

# MESSAGES (to console)
MESSAGE_CANT_CONNECT = "Не удалось подключиться к последовательному порту."
MESSAGE_CLOSE_WINDOW = "Закрытие окна"
