from graphics import *
import math
class Checker:
    def __init__(self, box, boxPoints, piece, king, side, id, win):
        self.box = box
        self.boxPoints = boxPoints
        self.isKing = False
        self.piece = piece
        self.king = king
        self.side = side
        self.id = id
        self.win = win

    def calcDyDx(self, newBox):
        dy = self.boxPoints[newBox[0]][newBox[1]].getY() - self.boxPoints[self.box[0]][self.box[1]].getY()
        dx = self.boxPoints[newBox[0]][newBox[1]].getX() - self.boxPoints[self.box[0]][self.box[1]].getX()
        return(dy, dx)

    def moveTo(self, newBox):
        if(self.side == 'bottom' and newBox[0] == 0):
            self.makeKing()
        elif(self.side == 'top' and newBox[0] == 7):
            self.makeKing()
        dy, dx = self.calcDyDx(newBox)
        if(not self.isKing):
            self.piece.move(dx, dy)
        else:
            self.king.move(dx, dy)
        self.box = newBox

    def removePiece(self):
        self.piece.undraw()

    def makeKing(self):
        if(not self.isKing):
            self.removePiece()
            self.isKing = True
            self.king.draw(self.win)
            newBox = self.box
            self.box = (0,0)
            self.moveTo(newBox)

class Board:
    def __init__(self, boxPoints, hasPiece, markers, gameWin):
        self.hasPiece = hasPiece
        self.boxPoints = boxPoints
        self.gameWin = gameWin
        self.whosTurn = 'top'
        self.markers = markers
        self.markersShown = []

    def getBox(self, point):
        x = math.floor(point.getX()/100)
        y = math.floor(point.getY()/100)
        if((y%2 == 0 and x%2 == 0) or (y%2 == 1 and x%2 == 1)):
            return(y,math.floor(x/2))
        else:
            return None

    def setWhosTurn(self):
        if(self.whosTurn == 'top'):
            self.whosTurn = 'bottom'
        else:
            self.whosTurn = 'top'
        return(self.whosTurn)

    def getHasPiece(self, box):
        return(self.hasPiece[box[0]][box[1]])

    def setHasPiece(self, box, value):
        self.hasPiece[box[0]][box[1]] = value

    def getPieceBetween(self, squareTo, squareFrom):
        yDir = squareTo[0]-squareFrom[0]
        xDir = squareTo[1]-squareFrom[1]
        isEven = True
        box = (0,0)
        if(squareFrom[0]%2 != 0):
            isEven = False

        if(xDir>0 and yDir>0):#++
            if(not isEven):
                box = (squareFrom[0]+1, squareFrom[1]+1)
            elif(isEven):
                box = (squareFrom[0]+1, squareFrom[1])
        elif(xDir>0 and yDir<0):#+-
            if(not isEven):
                box = (squareFrom[0]-1, squareFrom[1]+1)
            elif(isEven):
                box = (squareFrom[0]-1, squareFrom[1])
        elif(xDir<0 and yDir>0):#-+
            if(isEven):
                box = (squareFrom[0]+1, squareFrom[1]-1)
            elif(not isEven):
                box = (squareFrom[0]+1, squareFrom[1])
        elif(xDir<0 and yDir<0):#--
            if(isEven):
                box = (squareFrom[0]-1, squareFrom[1]-1)
            elif(not isEven):
                box = (squareFrom[0]-1, squareFrom[1])
        return(self.getHasPiece(box))

    def removeIds(self, ids, bottom, top):
        for i in range(len(ids)):
            if(ids[i][0] == 't'):
                self.setHasPiece(top[ids[i]].box, 0)
            elif(ids[i][0] == 'b'):
                self.setHasPiece(bottom[ids[i]].box, 0)

    def showMarker(self, boxClicked):
        try:
            whichMarker = boxClicked[0]*4+boxClicked[1]
        except TypeError:
            return None
        if whichMarker in self.markersShown:
            return None
        self.markers[whichMarker].draw(self.gameWin)
        self.markersShown.append(whichMarker)

    def hideMarkers(self):
        for i in range(0, len(self.markersShown)):
            self.markers[self.markersShown[i]].undraw()
        self.markersShown = []

class ScoreBoard:
    def __init__(self, scoreWin, scoreTop, scoreBottom, divider, topColor, bottomColor, gameMessage):
        self.scoreWin = scoreWin
        self.scoreTop = scoreTop
        self.scoreBottom = scoreBottom
        self.divider = divider
        self.topColor = topColor
        self.bottomColor = bottomColor
        self.gameMessage = gameMessage

    def changeScore(self, side, increase):
        if (side == 'top'):
            self.scoreTop.setText(int(self.scoreTop.getText())+increase)
        elif (side == 'bottom'):
            self.scoreBottom.setText(int(self.scoreBottom.getText())+increase)

    def setDivider(self, turn):
        if(turn == 'top'):
            self.divider.setFill(self.topColor)
        elif(turn == 'bottom'):
            self.divider.setFill(self.bottomColor)

    def setGameMessage(self, message):
        self.gameMessage.setText(message)


def init():
    scoreWin = GraphWin('Score Board', 400, 220)
    titleTop = Text(Point(100,20), 'Top Score')
    titleBottom = Text(Point(300,20), 'Bottom Score')
    scoreTop = Text(Point(100,50), '0')
    scoreBottom = Text(Point(300,50), '0')
    instructions = Text(Point(200, 110), 'Click on a piece and the squares \n it will move through to get to its\n final destination.\n Press enter to end selection.')
    divider = Rectangle(Point(0,150), Point(400,158))
    gameMessage = Text(Point(200, 180), 'Game messages appear here.')

    gameWin = GraphWin('Checkers', 800, 800)
    color = 'darkgreen'
    color1 = 'tan'
    color2 = 'brown'
    p1Color = 'black'
    p2Color = 'red'
    kingColor1 = 'yellow'
    kingColor2 = 'blue'
    radius = 45
    boxPoints = []
    top = {}
    bottom = {}
    markers = []
    hasPiece = []
#make score board
    titleTop.draw(scoreWin)
    titleBottom.draw(scoreWin)
    scoreTop.draw(scoreWin)
    scoreBottom.draw(scoreWin)
    instructions.draw(scoreWin)
    divider.setFill(p1Color)
    divider.draw(scoreWin)
    gameMessage.draw(scoreWin)
#make board
    for y in range(0,8):
        row = []
        pointsRow = []
        for x in range(0,8):
            if(y%2 == 0 and x == 0):
                color = color1
            elif(y%2 == 1 and x == 0):
                color = color2
            thisBox = Rectangle(Point(x*100,y*100), Point((x+1)*100, (y+1)*100))
            thisBox.setFill(color)
            thisBox.draw(gameWin)
            if((y%2 == 0 and x%2 == 0) or (y%2 != 0 and x%2 != 0)):
                boxCenter = thisBox.getCenter()
                pointsRow.append(boxCenter)
                thisMarker = Circle(boxCenter, 10)
                thisMarker.setFill('white')
                markers.append(thisMarker)
                row.append(0)
            if(color == color2):
                color = color1
            else:
                color = color2
        hasPiece.append(row)
        boxPoints.append(pointsRow)
# make top pieces
    for y in range(0,3):
        for x in range(0, 4):
            thisPiece = Circle(boxPoints[y][x], radius)
            thisPiece.setFill(p1Color)
            thisPiece.draw(gameWin)
            thisKing = Circle(boxPoints[0][0], radius)
            thisKing.setFill(kingColor1)
            id = 't'+str(4*y+x)
            checker = Checker((y,x), boxPoints, thisPiece, thisKing, 'top', id, gameWin)
            top[id] = checker
            hasPiece[y][x] = id
#make bottom pieces
    for y in range(0,3):
        for x in range(0, 4):
            thisPiece = Circle(boxPoints[y+5][x], radius)
            thisPiece.setFill(p2Color)
            thisPiece.draw(gameWin)
            thisKing = Circle(boxPoints[0][0], radius)
            thisKing.setFill(kingColor2)
            id = 'b'+str(4*y+x)
            checker = Checker((y+5,x), boxPoints, thisPiece, thisKing, 'bottom', id, gameWin)
            bottom[id] = checker
            hasPiece[y+5][x] = id
    return(boxPoints, top, bottom, markers, gameWin, hasPiece, scoreTop, scoreBottom, divider, p1Color, p2Color, gameMessage, scoreWin)

def mainLoop(notDone, board, top, bottom, scoreBoard):
    while(notDone):
        squares = getInputs(board, top, bottom)
        isValid, piecesToRemove = validateMove(board, top, bottom, squares, scoreBoard)
        if(not isValid):
            continue
        movePiece(board, squares, bottom, top)
        removePieces(piecesToRemove, top, bottom, board, scoreBoard)

def getInputs(board, top, bottom):
    squares = []
    board.gameWin._setHasReturn(False)
    while(not board.gameWin.hasReturn):
        mouseData = board.gameWin.getMouse()
        if(mouseData != 'Return'):
            boxClicked = board.getBox(mouseData)
            squares.append(boxClicked)
            board.showMarker(boxClicked)
        else:
            board.hideMarkers()
    board.gameWin._setHasReturn(False)
    return(squares)

def validateMove(board, top, bottom, squares, scoreBoard):
    squareTo = 0
    try:
        squareTo = squares[len(squares)-1]
    except IndexError:
        scoreBoard.setGameMessage('You pressed enter without \nselecting a move.')
        return (False, [])
    squareFrom = squares[0]
    if(len(squares)<2):
        scoreBoard.setGameMessage('Must select a piece and \nsubsequent moves to destination.')
        return (False, [])
    if(len(squares)!=len(set(squares))):
        scoreBoard.setGameMessage('You clicked on the same square twice.')
        return (False, [])
    if(squareFrom == None):
        scoreBoard.setGameMessage('Invalid square.')
        return (False, [])
    elif(board.getHasPiece(squareFrom) == 0):
        scoreBoard.setGameMessage('No piece found.')
        return (False, [])
    if(board.whosTurn[0] != board.getHasPiece(squareFrom)[0]):
        scoreBoard.setGameMessage('Not your turn.')
        return (False, [])
    if(squareTo == None):
        scoreBoard.setGameMessage('Invalid square.')
        return (False, [])
    elif(board.getHasPiece(squareTo) != 0):
        scoreBoard.setGameMessage('There is a piece in that box.')
        return (False, [])

    pieceToMove = board.getHasPiece(squareFrom)
    if(squareTo[0] <= squareFrom[0]):
        if(pieceToMove[0] == 't' and not top[pieceToMove].isKing):
            scoreBoard.setGameMessage('Piece is not a king.')
            return (False, [])
    if(squareTo[0] >= squareFrom[0]):
        if(pieceToMove[0] == 'b' and not bottom[pieceToMove].isKing):
            scoreBoard.setGameMessage('Piece is not a king.')
            return (False, [])
    scoreBoard.setGameMessage('Game messages appear here.')
    piecesToRemove = findDeadPieces(board, top, bottom, squares)
    if(piecesToRemove == 'invalid'):
        scoreBoard.setGameMessage('Invalid move.')
        return (False, [])
    return(True, piecesToRemove)

def findDeadPieces(board, top, bottom, squares):
    piecesToRemove = []
    for i in range(0, len(squares)):
        squareFrom = squares[i]
        squareTo = (0,0)
        try:
            squareTo = squares[i+1]
        except:
            break

        yDist = math.fabs(squareFrom[0]-squareTo[0])
        xDist = math.fabs(squareFrom[1]-squareTo[1])
        #single space moves
        if(i!=0):
            if(yDist==1 and (xDist==0 or xDist==1)):
                return('invalid')
        elif(i==0):
            if(yDist==1 and (xDist==0 or xDist==1) and len(squares)==2):
                return[]
            else:
                pass
        #end single space moves
        #more than double jump (all invalid)
        if(yDist>2 or xDist>1):
            return('invalid')
        #end more than double jump
        #jumps (double space moves)
        if(yDist==2 and xDist==1):
            whosTurn = board.whosTurn
            spotJumped = board.getPieceBetween(squareTo, squareFrom)
            if(spotJumped == 0):
                return('invalid')
            elif(spotJumped[0] == board.whosTurn[0]):
                return('invalid')
            else:
                piecesToRemove.append(spotJumped)
        #end jumps
    return(piecesToRemove)

def movePiece(board, squares, bottom, top):
    squareTo = squares[len(squares)-1]
    squareFrom = squares[0]
    id = board.getHasPiece(squareFrom)
    pieceToMove = None
    if (id[0] == 't'):
        pieceToMove = top[id]
    elif(id[0] == 'b'):
        pieceToMove = bottom[id]
    pieceToMove.moveTo(squareTo)
    board.setHasPiece(squareTo, id)
    board.setHasPiece(squareFrom, 0)

def removePieces(piecesToRemove, top, bottom, board, scoreBoard):
    updateScoreBoard(scoreBoard, board, len(piecesToRemove))
    if(len(piecesToRemove) == 0):
        return None
    for i in range(0, len(piecesToRemove)):
        if (piecesToRemove[i][0] == 't'):
            top[piecesToRemove[i]].removePiece()
        elif(piecesToRemove[i][0] == 'b'):
            bottom[piecesToRemove[i]].removePiece()
    board.removeIds(piecesToRemove, bottom, top)

def updateScoreBoard(scoreBoard, board, increase):
    whosTurn = board.setWhosTurn()
    scoreBoard.setDivider(whosTurn)
    if(whosTurn == 'top'):
        scoreBoard.changeScore('top', increase)
    elif(whosTurn == 'bottom'):
        scoreBoard.changeScore('bottom', increase)


def main():
    boxPoints, top, bottom, markers, gameWin, hasPiece, scoreTop, scoreBottom, divider, p1Color, p2Color, gameMessage, scoreWin = init()
    board = Board(boxPoints, hasPiece, markers, gameWin)
    scoreBoard = ScoreBoard(scoreWin, scoreTop, scoreBottom, divider, p1Color, p2Color, gameMessage)
    notDone = True
    try:
        mainLoop(notDone, board, top, bottom, scoreBoard)
    except GraphicsError:
        gameWin.close()

if __name__ == '__main__':
    main()
