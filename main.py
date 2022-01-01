from Field import Field


def main():
    field = Field()
    somebody_wins = False
    moves = 0
    player = False
    print_field = True
    while not somebody_wins and moves < 42:
        if print_field:
            print(field)
            print("Player {0}, please type the number of the column where you'd lke to put your chip: ".format(player + 1))
        col = input()
        if not col.isdigit() or 0 > int(col) or 7 <= int(col):
            print("Please, type the correct number of the column")
            print_field = False
            continue
        col = int(col)
        turn_result = field.turn(col, player)
        if turn_result == 2:
            print("Please, type the correct number of the column")
            print_field = False
            continue
        print_field = True
        somebody_wins = turn_result
        player ^= 1
        moves += 1
        print(*field.used)
    if somebody_wins:
        print("Player {0} wins! Congrats!!!".format((player ^ 1) + 1))
    else:
        print("Draw!")
    print(field)


if __name__ == "__main__":
    main()
