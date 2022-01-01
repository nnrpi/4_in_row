from Field import Field
from tkinter import *
from typing import Union

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 650

root = Tk()
c = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
text_label = Label(text="Player 1, please type the number of the column\nwhere you'd lke to put your chip:",
                   justify=LEFT,
                   bg="#BDDCFF",
                   borderwidth=2, relief="solid")
entry_col = Entry(width=10, borderwidth=2, relief="solid")

field = Field()
somebody_wins = False
moves = 0
player = False
print_field = True


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
    player ^= 1
    moves += 1
    return somebody_wins


def make_turn(col: Union[int, str]) -> None:
    result = try_turn(col)
    if result != 2:
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
        c.tag_bind(cell, '<ButtonPress-1>', on_click_cell)
        print(field)
        if somebody_wins:
            text_label['text'] = "Player {0} wins! Congrats!!!".format((player ^ 1) + 1)
        if moves == 42:
            text_label['text'] = "Draw!"


def on_change(entry_col) -> None:
    if somebody_wins or moves >= 42:
        entry_col.widget.delete(0, 'end')
        return
    col = entry_col.widget.get()
    entry_col.widget.delete(0, 'end')
    make_turn(col)


def on_click_cell(event) -> None:
    if somebody_wins or moves >= 42:
        return
    col = event.x // 100 + 1
    make_turn(col)


def main():
    root.resizable(width=False, height=False)
    c.create_rectangle(0, 0, 700, 600, fill='#8D84FF')
    # cells = [
    #     [c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill="white", width=3) for row in
    #      range(6)]
    #     for col in range(7)]
    for col in range(7):
        for row in range(6):
            cell = c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill="white", width=3)
            c.tag_bind(cell, '<ButtonPress-1>', on_click_cell)
    for col in range(7):
        number_frame = Frame(root, width=100, height=50, bg="white")
        number_frame.pack_propagate(False)
        number_frame.place(x=col * 100, y=601)
        number = Label(number_frame, text=str(col + 1), bg='white', fg='black', font='Arial, 32')
        number.place(relx=0.5, rely=0.5, anchor=CENTER)
    text_label.place(x=710, y=10)
    entry_col.place(x=1050, y=27)
    entry_col.bind("<Return>", on_change)
    c.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
