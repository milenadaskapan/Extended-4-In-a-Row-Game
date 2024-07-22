class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
    
    def num_free_positions_in_column(self, column):
        col = self.items[column]
        free=self.size
        for i in range(self.size):
            if col[i] !=0:
                free-=1
        return free
    def free_slots_as_close_to_middle_as_possible(self):
        new_list = []
        
        for i in range(self.size):
                check = GameBoard.num_free_positions_in_column(self, i)
                if check != 0:
                    new_list+=[i]
        middle = float((self.size-1)/2)
        
        if len(new_list) ==0 or len(new_list) ==1:
            return new_list
        else:
            for j in range(len(new_list)):
                for i in range(len(new_list)-1):

                    first_middle = abs(float(middle - new_list[i]))
                    compare_middle = abs(float(middle -new_list[i+1]))
                    
                    if first_middle > compare_middle:
                        new_list[i], new_list[i+1] = new_list[i+1], new_list[i]
                    elif compare_middle == first_middle:
                        if new_list[i] > new_list[i+1]:
                            new_list[i], new_list[i+1] = new_list[i+1], new_list[i]
                    
        return new_list
    
    def game_over(self):
        check = 0
        for i in range(self.size):
            col = GameBoard.num_free_positions_in_column(self, i)
            check+=col
        if check == 0:
            return True
        else:
            return False
    
    def display(self):
        
        new_string = ['']*self.size
        line = ''
        
        for i in range(self.size):
            line+=str(i) + ' '
            col = self.items[i]
            for j in range(self.size):
                position = col[j]
                if position ==0:
                    new_string[j] += '  '
                elif position ==1:
                    new_string[j]+='o '
                elif position ==2:
                    new_string[j]+='x '
                
        for i in range(len(new_string)-1,-1,-1):
            print(new_string[i])
        
        dashes = '-' * (self.size*2 -1)
        print(dashes)
        print(line)
        print("Points player 1:", self.points[0])
        print("Points player 2:", self.points[1])
    
    
    def add(self, column, player):
        entry = self.num_entries[column]
        row = self.num_entries[column]
        if entry>=self.size or column<0 or column>= self.size:
            return False
        else:
            self.items[column][row] = player
            self.num_entries[column]+= 1
            self.points[player-1] += GameBoard.num_new_points(self, column, row, player)
            
        return True
    
    def num_new_points(self, column, row, player):
        new = 0
        if column >= self.size or row>=self.size or player>2 or player<1:
            raise ValueError("Faulty")
        row_index = row
        col_count=0
        while (self.items[column][row_index] == player) and (row_index>=0):
            row_index-=1
            col_count+=1
        if col_count>=4:
            new+=1
                    

        column_left = column
        row_count = 0
        left = 0
        right = 0
        while (self.items[column_left][row]==player) and (column_left>=0):
            if column_left!=column:
                left+=1
            row_count+=1
            column_left-=1
        column_right = column
        while (column_right<=(self.size-1)) and ((self.items[column_right][row])==player) :
            if column_right != column:
                right+=1
            row_count+=1
            column_right+=1

        if row_count >=4:
            if right>3:
                right=3
            if left>3:
                left=3
            new+=(left+right+1)-3


        diagonal_row = row
        diagonal_column = column
        count = 0
        left = 0
        right = 0
        
        while ((diagonal_row<=(self.size-1)) and (self.items[diagonal_column][diagonal_row] == player) and (diagonal_column>=0)):
            if diagonal_column!=column:
                left+=1
            count+=1
            diagonal_row +=1
            diagonal_column -=1
        
        diagonal_row = row
        diagonal_column = column
        
        while ((diagonal_column<=(self.size-1) and (self.items[diagonal_column][diagonal_row] == player)) and (diagonal_row>=0)):
            if diagonal_column!= column:
                right+=1
            count+=1
            diagonal_row-=1
            diagonal_column+=1
        if count>=4:
            if right>3:
                right=3
            elif right == -1:
                right = 0
            if left>3:
                left=3
            new+=(left+right+1)-3

        diagonal_row = row
        diagonal_column = column
        count = 0
        left = 0
        right = 0
        
        while ((self.items[diagonal_column][diagonal_row] == player) and (diagonal_column>=0) and (diagonal_row>=0)):
            if diagonal_column!=column:
                left+=1
            count+=1
            diagonal_row -=1
            diagonal_column -=1

        
        diagonal_row = row
        diagonal_column = column
        
        while ((diagonal_column<=(self.size-1)) and (diagonal_row<=(self.size-1)) and (self.items[diagonal_column][diagonal_row] == player)):
            if diagonal_column!= column:
                right+=1
            count+=1
            diagonal_row+=1
            diagonal_column+=1
        
        if count>=4:
            if right>3:
                right=3
            elif right ==-1:
                right = 0
            if left>3:
                left=3
            new+=(left+right+1)-3
        return new
    
    def num_free_positions_in_column(self, column):
        col = self.items[column]
        free=self.size
        for i in range(self.size):
            if col[i] !=0:
                free-=1
        return free
    

    
    def column_resulting_in_max_points(self, player):
        if GameBoard.game_over(self) == False:
            
            largest_points = 0 
            slot = GameBoard.free_slots_as_close_to_middle_as_possible(self)[0]

            for column in GameBoard.free_slots_as_close_to_middle_as_possible(self):
                row = self.num_entries[column]
                GameBoard.add(self, column, player)
                points = GameBoard.num_new_points(self, column, row, player)

                self.items[column][row] = 0
                self.num_entries[column]-= 1
                self.points[player-1] -= points
                    
                if points>largest_points:
                    largest_points = points
                    slot = column
        return (slot, largest_points)
class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(8)
game.play()   