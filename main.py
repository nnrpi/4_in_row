from Field import Field
from tkinter import *

root = Tk()
c = Canvas(root, width=1200, height=600, bg='white')
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


def make_turn(col: str) -> int:
    global player
    global moves
    global somebody_wins
    if not col.isdigit() or 0 > int(col) or 7 <= int(col):
        text_label['text'] = "Please, type the correct number of the column"
        return 2
    col = int(col)
    turn_result = field.turn(col, player)
    if turn_result == 2:
        text_label['text'] = "Please, type the correct number of the column"
        return 2
    somebody_wins = turn_result
    player ^= 1
    moves += 1
    return somebody_wins


def on_change(entry_col):
    if somebody_wins or moves >= 42:
        entry_col.widget.delete(0, 'end')
        return
    col = entry_col.widget.get()
    entry_col.widget.delete(0, 'end')
    result = make_turn(col)
    if result != 2:
        text_label['text'] = "Player {0}, please type the number of the column\nwhere you'd lke to put your chip:".format(player + 1)
        col = int(col)
        row = 6 - field.used[col]
        if player == 1:
            colour = "green"
        else:
            colour = "red"
        c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill=colour, width=3)
        print(field)
        if somebody_wins:
            text_label['text'] = "Player {0} wins!\nCongrats!!!".format((player ^ 1) + 1)
        if moves == 42:
            text_label['text'] = "Draw!"


def draw_canvas():
    c.pack()
    c.create_rectangle(0, 0, 700, 600, fill='#8D84FF')
    for col in range(7):
        for row in range(6):
            c.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill="white", width=3)
    text_label.place(x=710, y=10)
    entry_col.place(x=1050, y=27)
    entry_col.bind("<Return>", on_change)
    root.mainloop()


def main():
    draw_canvas()
    global somebody_wins
    global moves
    # while not somebody_wins and moves < 42:
        # if print_field:
        #     print(field)
        #     print("Player {0}, please type the number of the column where you'd lke to put your chip: ".format(player + 1))
        # col = input()
        # if not col.isdigit() or 0 > int(col) or 7 <= int(col):
        #     print("Please, type the correct number of the column")
        #     print_field = False
        #     continue
        # col = int(col)
        # turn_result = field.turn(col, player)
        # if turn_result == 2:
        #     print("Please, type the correct number of the column")
        #     print_field = False
        #     continue

        # print_field = True
        # somebody_wins = turn_result
        # player ^= 1
        # moves += 1
        # print(*field.used)
    if somebody_wins:
        print("Player {0} wins! Congrats!!!".format((player ^ 1) + 1))
    else:
        print("Draw!")
    print(field)


if __name__ == "__main__":
    main()
