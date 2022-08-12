from random import randint


class Cell:

    def __init__(self, around_mines=0, mine=0):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    '''Инициализация значений: N-размер поля, M-кол. мин'''

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.pole = [[Cell() for _ in range(N)] for _ in range(N)]
        self.init()

    def init(self):
        set_cords = list()
        combinations = [[0, 1], [0, -1], [1, 0], [-1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        counter = self.M
        '''Раставляем мины по полю в случайном порядке '''
        if counter <= self.N ** 2:
            while counter != 0:
                i, j = randint(0, self.N - 1), randint(0, self.N - 1)
                if self.pole[i][j].mine == 0:
                    self.pole[i][j].mine = '*'
                    set_cords.append((i, j))
                    counter -= 1
                else:
                    continue
        '''Подсчитываем количество мин вокруг клетки (которая не является миной)'''
        for cords in set_cords:
            i, j = cords
            for l in combinations:
                x, y = l
                if (-1 < x + i < len(self.pole)) and (-1 < y + j < len(self.pole)):
                    if self.pole[x + i][j + y].mine != '*':
                        self.pole[x + i][j + y].around_mines += 1

    def show(self):
        '''Выводим игровое поле, где #-клетка скрыта'''
        if self.N * self.N <= self.M:
            print('Количество мин превышает размер поля')
        else:
            for str_pole in self.pole:
                print(*['#' if x.fl_open == False else x.mine if x.mine == '*' else x.around_mines for x in str_pole])

    def show_all_zero(self):
        '''Открываем скртые клетки, если они пусты'''
        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].around_mines == 0 and self.pole[i][j].mine != '*':
                    self.pole[i][j].fl_open = True
    def show_all_cells(self):
        '''Отыкрываем все клетки'''
        for i in range(self.N):
            for j in range(self.N):
                self.pole[i][j].fl_open = True
    def getPlayerMove(self):
        '''Получаем значения, которые вводит пользователь'''
        ivent_loop = True
        while ivent_loop:
            try:
                print('Введите координаты клетки')
                x, y = map(int, input().split())
            except ValueError:
                print('Вы ввели что-то неверно')
                continue
            x = x - 1
            y = y - 1
            if not (0 <= x < self.N) and not (0 <= y < self.N):
                print('Вы ввели координты за пределами поля')
                continue
            ivent_loop = False
            return x, y

    def game_status(self):
        '''Статус игры, пока мы не наступили на мину игра продолжается'''
        GamePole.show(self)
        print()
        i, j = GamePole.getPlayerMove(self)

        if self.pole[i][j].mine == '*':
            return -1
        elif self.pole[i][j].around_mines != 0:
            self.pole[i][j].fl_open = True
        else:
            GamePole.show_all_zero(self)
        counter_open_cell = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].fl_open:
                    counter_open_cell += 1
        if counter_open_cell == self.N * self.N - self.M:
            return 1
        return 0


size_pole = int(input('Размер поля: ', ))
mines = int(input('Количество мин на поле: ', ))

pole_game = GamePole(size_pole, mines)

while True:
    res = pole_game.game_status()
    if res == -1:
        print('---------------------------')
        print('LOSE. Вы наступили на мину')
        pole_game.show_all_cells()
        pole_game.show()
        break
    elif res == 1:
        print('---------------------------')
        print('Вы выиграли')
        pole_game.show_all_cells()
        pole_game.show()
        break
