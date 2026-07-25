
class Piece:
    def __init__(self,row,col,color,king = False):
        """

        :type image: object
        """
        self.row = row
        self.col = col
        self.color= color
        self.king = king

        self.rect = None