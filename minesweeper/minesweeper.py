import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #if the count of mines is equal to the count of cells, all cells are mines
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        #assume that self.cells exclude mines and moves made
        #if the count of mines is zero, all cells are safe
   
        if self.count == 0:
            return self.cells
        else:
            return set()    

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        
        #if cell is in the sentence, remove it
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        #add cell to known mines
        prevMine = self.known_mines()
        prevMine.add(cell)
        
        #update sentence
        self.cells = prevMine
        self.count = len(prevMine)
        """
        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
            else:
                self.count -= 1
        self.cells = newCells
        
        
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #if cell is in the sentence, remove it
        if cell in self.cells:
            self.cells.remove(cell)
            #self.safes.add(cell) #given?


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #raise NotImplementedError

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        #   2) mark the cell as safe
        self.mark_safe(cell)

        #    3) add a new sentence to the AI's knowledge base
        #       based on the value of `cell` and `count`

        neighbours, count = self.get_cell_neighbors(cell, count)
        sentence = Sentence(neighbours, count)
        self.knowledge.append(sentence) 

    # Conclusion
        new_inferences = []
        for s in self.knowledge:
            if s == sentence:
                continue
            elif s.cells.issuperset(sentence.cells):
                setDiff = s.cells-sentence.cells

                # Known safes
                if s.count == sentence.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                
                # Known mines
                elif s.count - sentence.count == len(setDiff):
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)

                # New inferences
                else:
                    new_inferences.append(Sentence(setDiff, s.count - sentence.count))
            
            elif sentence.cells.issuperset(s.cells):
                setDiff = sentence.cells-s.cells

                # Known safes
                if sentence.count == s.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)

                # Known mines
                elif sentence.count - s.count == len(setDiff):
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)

                # New inferences
                else:
                    new_inferences.append(Sentence(setDiff, sentence.count - s.count))

        self.knowledge.extend(new_inferences)
        self.remove_dups()
        self.remove_sures()

        #    4) mark any additional cells as safe or as mines
        #       if it can be concluded based on the AI's knowledge base
        #       for each sentence in the knowledge base

        #initialize a set of safe and mine cells
        safecell = set()
        minecell = set()

        for sentence in self.knowledge:

            safeSentence = sentence.known_safes()
            if len(safeSentence) > 0:
                for cell in safeSentence:
                    safecell.add(cell)

            mineSentence = sentence.known_mines()
            if len(sentence.known_mines()) > 0: 
                for cell in mineSentence:
                    minecell.add(cell)


        #    5) add any new sentences to the AI's knowledge base
        #       if they can be inferred from existing knowledge
        #use subset knowledge to recount sentences, remove duplicates
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 is sentence2:
                    continue
                if sentence1 == sentence2:
                    self.knowledge.remove(sentence2)
                elif sentence1.cells.issubset(sentence2.cells):
                    new_knowledge = Sentence(
                        sentence2.cells - sentence1.cells,
                        sentence2.count - sentence1.count)
                    if new_knowledge not in self.knowledge:
                        self.knowledge.append(new_knowledge)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_steps = self.safes - self.moves_made
        if len(possible_steps) > 0:
            return possible_steps.pop()
        else:
            return None
        



    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)
            
    def get_cell_neighbors(self, cell, count):
        i, j = cell
        neighbors = []

        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if (row >= 0 and row < self.height) \
                and (col >= 0 and col < self.width) \
                and (row, col) != cell \
                and (row, col) not in self.safes \
                and (row, col) not in self.mines:
                    neighbors.append((row, col))
                if (row, col) in self.mines:
                    count -= 1

        return neighbors, count
        
    def remove_dups(self):
        unique_knowledge = []
        for s in self.knowledge:
            if s not in unique_knowledge:
                unique_knowledge.append(s)
        self.knowledge = unique_knowledge

    def remove_sures(self):
        final_knowledge = []
        for s in self.knowledge:
            final_knowledge.append(s)
            if s.known_mines():
                for mineFound in s.known_mines():
                    self.mark_mine(mineFound)
                final_knowledge.pop(-1)
            elif s.known_safes():
                for safeFound in s.known_safes():
                    self.mark_safe(safeFound)
                final_knowledge.pop(-1)
        self.knowledge = final_knowledge