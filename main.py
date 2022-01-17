from Field import Field
from tkinter import *
from typing import Union
from alpha_beta import make_alpha_beta

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 650

root = Tk()
root.geometry("1200x650")
c = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
text_label = Label(c)
entry_col = Entry(width=10, borderwidth=1, relief="solid")
button_no_bot = Button()
button_with_bot = Button()

field = Field()
somebody_wins = False
moves = 0
player = False
print_field = True
is_bot_here = False


def try_turn(col: Union[int, str]) -> int:
    global player
    global moves
    global somebody_wins
    if (isinstance(col, str) and not col.isdigit()) or 1 > int(col) or int(col) > 7:
        text_label['text'] = "Please, type the correct number of the column"
        return 2
    col = int(col) - 1
    turn_result = field.turn(col, player)
    if turn_result == 2:
        text_label['text'] = "Please, type the correct number of the column"
        return 2
    somebody_wins = turn_result
    if not is_bot_here:
        player ^= 1
    moves += 1
    return somebody_wins


def make_turn(col: Union[int, str]) -> None:
    result = try_turn(col)
    if result != 2:
        if not is_bot_here:
            text_label[
                'text'] = "Player {0}, please type the number of the column\nwhere you'd lke to put your chip:".format(
                player + 1)
        col = int(col) - 1
        row = 6 - field.used[col]
        if player == 1:
            colour = "green"
        else:
            colour = "red"
        cell = c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill=colour, width=3)
        if is_bot_here:
            c.tag_bind(cell, '<ButtonPress-1>', on_click_cell_with_bot)
        else:
            c.tag_bind(cell, '<ButtonPress-1>', on_click_cell_no_bot)
        c.update()
        print(field)
        if somebody_wins:
            text_label['text'] = "Player {0} wins! Congrats!!!".format((player ^ 1) + 1)
        if moves == 42:
            text_label['text'] = "Draw!"


def make_bot_turn() -> None:
    if field.check_win(True):
        text_label['text'] = "Bot wins! Congrats!!!"
        return
    if field.check_win(False):
        return
    global moves
    if moves == 42:
        text_label['text'] = "Draw!"
        return
    turn_res, col, scores = make_alpha_beta(field)
    print(scores)
    if -turn_res not in scores:
        print("ahtung!!!")
        exit(0)
    col = scores.index(-turn_res)
    field.turn(col, True)
    moves += 1
    print(turn_res, col)
    row = 6 - field.used[col]
    colour = "green"
    cell = c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill=colour, width=3)
    c.tag_bind(cell, '<ButtonPress-1>', on_click_cell_with_bot)
    c.update()
    print(field)
    if field.check_win(True):
        text_label['text'] = "Bot wins! Congrats!!!"
        return
    if moves == 42:
        text_label['text'] = "Draw!"
        return
    if somebody_wins:
        text_label['text'] = "Player {0} wins! Congrats!!!".format(player + 1)
    if moves == 42:
        text_label['text'] = "Draw!"


def on_change_with_bot(entry_col) -> None:
    if somebody_wins or moves >= 42:
        entry_col.widget.delete(0, 'end')
        return
    col = entry_col.widget.get()
    entry_col.widget.delete(0, 'end')
    make_turn(col)
    make_bot_turn()


def on_change_no_bot(entry_col) -> None:
    if somebody_wins or moves >= 42:
        entry_col.widget.delete(0, 'end')
        return
    col = entry_col.widget.get()
    entry_col.widget.delete(0, 'end')
    make_turn(col)


def on_click_cell_with_bot(event) -> None:
    print("moves: ", moves)
    print("-" * 40)
    if somebody_wins or moves >= 42:
        return
    col = event.x // 100 + 1
    make_turn(col)
    make_bot_turn()


def on_click_cell_no_bot(event) -> None:
    print("moves: ", moves)
    print("-" * 40)
    if somebody_wins or moves >= 42:
        return
    col = event.x // 100 + 1
    make_turn(col)


def start_mains():
    c['width'] = CANVAS_WIDTH
    c['height'] = CANVAS_HEIGHT
    entry_col.pack()
    global text_label
    text_label.config(text="Player 1, please type the number of the column\nwhere you'd lke to put your chip:",
                      font=("Courier", 12), justify=LEFT)
    # text_label['bg'] = "#BDDCFF"
    # text_label['borderwidth'] = 2
    # text_label['relief'] = "solid"
    button_no_bot.destroy()
    button_with_bot.destroy()
    c.create_rectangle(0, 0, 700, 600, fill='#8D84FF')
    text_label.place(x=710, y=10)
    entry_col.place(x=1050, y=27)
    for col in range(7):
        number_frame = Frame(root, width=100, height=50, bg="white")
        number_frame.pack_propagate(False)
        number_frame.place(x=col * 100, y=601)
        number = Label(number_frame, text=str(col + 1), bg='white', fg='black', font='Arial, 32')
        number.place(relx=0.5, rely=0.5, anchor=CENTER)


def main_no_bot():
    start_mains()
    for col in range(7):
        for row in range(6):
            cell = c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill="white", width=3)
            c.tag_bind(cell, '<ButtonPress-1>', on_click_cell_no_bot)
    entry_col.bind("<Return>", on_change_no_bot)
    c.pack()


def main_with_bot():
    global is_bot_here
    is_bot_here = True
    start_mains()
    for col in range(7):
        for row in range(6):
            cell = c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill="white", width=3)
            c.tag_bind(cell, '<ButtonPress-1>', on_click_cell_with_bot)
    entry_col.bind("<Return>", on_change_with_bot)
    c.pack()


def main():
    root.resizable(width=False, height=False)
    global text_label
    text_label.config(text="Choose how you'd like to play:", justify=CENTER, bg="#BDDCFF", borderwidth=2,
                      relief="solid", font=("Courier", 40))
    text_label.place(x=500, y=20)
    text_label.pack()
    entry_col.pack_forget()
    button_with_bot.config(text="With bot", command=main_with_bot, font=("Courier", 44), bg="#E48A7F",
                           activebackground="#A1FF89")
    button_no_bot.config(text="With another player", command=main_no_bot, font=("Courier", 44), bg="#CD7FE4",
                         activebackground="#A1FF89")
    # button_no_bot.place(x=200, y=100)
    # button_with_bot.place(x=800, y=100)
    # c.update()
    c.pack()
    button_no_bot.pack()
    button_with_bot.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
