import json
class Node:
  def __init__(self, node, newBoard, isWinner, winner, value, nodesChilds=[],nodeFather=0):
    self.node = node
    self.newBoard = newBoard
    self.nodesChilds = nodesChilds
    self.isWinner = isWinner
    self.winner = winner
    self.value = value
    self.nodeFather = nodeFather
  def __str__(self):
    return f'node={self.node}, newBoard={self.newBoard}, nodesChilds={self.nodesChilds}, nodeFather={self.nodeFather}, isWinner={self.isWinner}, value={self.value}, winner={self.winner}'


board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
boards = [[(board,False)]]
voidSpaces = len([1 for i in range(len(board)) if board[i]==' '])
nodes = {'root':Node('root',board,False,None,0,[f'{1}-{i+1}'for i in range(8)],None)}


def win(board):
  sol = [
      [0,1,2],
      [3,4,5],
      [6,7,8],
      [0,3,6],
      [1,4,7],
      [2,5,8],
      [0,4,8],
      [6,4,2]
  ]
  for i in range(8):
    s = []
    for j in range(3):
      res = sol[i][j]
      s.append(board[res])
    [a,b,c] = s
    if a!=' ' and a==b and a==c:
      return True,a
  return False,None

def createBoards(currentBoard,w):
  turn = 'o'
  if w:
    return []
  full = len([1 for i in range(len(currentBoard)) if currentBoard[i]!=' '])
  if full%2!=0:
    turn = 'x'
  branches = len(currentBoard) - full
  newBoards = []
  squareUsed = []
  for n in range(branches):
    isWinner = False
    b = currentBoard.copy()
    for i in range(len(currentBoard)):
      if (currentBoard[i] == ' ') and ((i,turn) not in squareUsed):
        squareUsed.append((i,turn))
        b[i] = turn
        isWinner,winner = win(b)
        break
    newBoards.append((b,isWinner))
  return newBoards

def valuePlayed(win):
  match win:
    case 'x':
      return (1)
    case 'o':
      return (-1)
    case None:
      return 0

for branch in range(voidSpaces):
  branch = branch + 1
  listBoards = boards[len(boards)-1]
  blankSpaces = voidSpaces - branch
  boardsBranch = []
  num = 1
  child = 0
  for b in range(len(listBoards)):
    l = createBoards(listBoards[b][0],listBoards[b][1])
    for i in range(len(l)):
      father = f'{str(branch-1)}-{str(b+1)}'
      if branch == 1:
        father = 'root'
      listAdy = []
      newBoard = l[i][0]
      isWinner,winner = win(newBoard)
      value = valuePlayed(winner)
      if not isWinner:
        p = list(range(child*blankSpaces+1,((child+1)*blankSpaces)+1))
        listAdy = list(map(lambda x:f'{branch+1}-{x}',p))
        child = child+1
      node = f'{str(branch)}-{str(num)}'
      newNode = Node(node,newBoard,isWinner,winner,value,listAdy,father)
      nodes[node] = newNode
      num = num+1
    for o in range(len(l)):
      boardsBranch.append(l[o])
  boards.append(boardsBranch)

goodList = list(filter(lambda x: x.value!=-1 and x.nodesChilds==[] ,nodes.values()))
goodList = [ (goodList[e].node, goodList[e].isWinner) for e in range(len(goodList))]

tree = {'root':nodes['root']}

def buildTree(vert,v,initVert):
  newVert = nodes[vert].nodeFather
  tree[vert]=nodes[vert]
  tree[vert].value = v + tree[vert].value
  if newVert==initVert:
    return
  return buildTree(newVert,v,initVert)

def valueOption(initVert):
  for n in goodList:
    v = nodes[n[0]].value
    buildTree(n[0],v,initVert)

valueOption('root')

del nodes
for n in tree.keys():
  for v in tree[n].nodesChilds:
    if v not in tree:
      tree[n].nodesChilds = list(filter(lambda x: x!=v,tree[n].nodesChilds))
  tree[n] = vars(tree[n])

with open('tree.json', 'w') as file:
    json.dump(tree, file)