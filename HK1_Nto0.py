import sys

class Node:
    index = 0;
    value = 0;
    primitive = 2;
    len2leaf = 0;
    def __init__(self,index,value,primitive,len2leaf):
        self.index = index;
        self.value = value;
        self.primitive = primitive;
        self.len2leaf = len2leaf;
            
#Function primitive()
#args:
#       index: the index of current node
#       init_pos: the position of current node
#       prim: the primitive of current node
#       player: computer/human turn
#return:
#       0: computer lose
#       1: computer win
def primitive(index,init_pos,prim,player):
    global Gametree;
    if(prim == 2): # unknown
        if(init_pos > 0):   #left child exist
            # change the index and value of the left child
            GameTree[2*index+1].index = 2*index+1;
            GameTree[2*index+1].value = init_pos-1;
            # iteration->keep finding it's children's primitive
            LeftPrimitive = primitive(2*index+1,init_pos-1,2,(player+1)%2);
            # change the primitive of the left child
            GameTree[2*index+1].primitive = LeftPrimitive;
        else:
            LeftPrimitive = 0;
        if(init_pos > 1):   #right child exist
            # change the index and value of the right child
            GameTree[2*index+2].index = 2*index+2;
            GameTree[2*index+2].value = init_pos-2;
            # iteration->keep finding it's children's primitive
            RightPrimitive = primitive(2*index+2,init_pos-2,2,(player+1)%2);
            # change the primitive of the right child
            GameTree[2*index+2].primitive = RightPrimitive;
        else:
            RightPrimitive = 0;
            
        if(player == 0):    #Computer's turn
            if(init_pos == 0): # leaf node
                GameTree[index].len2leaf = 0;
                return 0;
            else:
                # change the length to root
                GameTree[index].len2leaf = max(GameTree[2*index+1].len2leaf,GameTree[2*index+2].len2leaf)+1;
                # return primitive
                if(LeftPrimitive+RightPrimitive>0):
                    return 1;
                else:
                    return 0;
        else:   #Human's turn
            if(init_pos == 0):  # leaf node
                GameTree[index].len2leaf = 0;
                return 1;
            else:
                # change the length to root
                GameTree[index].len2leaf = max(GameTree[2*index+1].len2leaf,GameTree[2*index+2].len2leaf)+1;
                # return primitive
                return (LeftPrimitive*RightPrimitive);
    else:
        return prim


#Function generate_moves()
#args:
#       primitive: the primitive of current node
#       index: the index of current node
#       player: current turn -> computer/human
#return:
#       0: take 1
#       1: take 2
#       2: win/lose
def generate_moves(primitive,index,player):
    global GameTree;
    if(GameTree[index].len2leaf == 0):
        return 2;
    else:
        if(player==0):
            if(primitive == 0): # doom to losing
                # choose a path that lose as low as possible
                if(GameTree[2*index+1].len2leaf >= GameTree[2*index+2].len2leaf):
                    return 0;
                else:
                    return 1;
            else:   # computer can win
                # choose a path that will win and win as quick as possible
                if(GameTree[2*index+1].primitive == GameTree[2*index+2].primitive): # choose a shortest path
                    if(GameTree[2*index+1].len2leaf <= GameTree[2*index+2].len2leaf):
                        return 0;
                    else:
                        return 1;
                else:   # choose a path that will win
                    if(GameTree[2*index+1].primitive == 1):
                        return 0;
                    else:
                        return 1;
        else:
            while(1):
                HumanTake = input("How many do you want to take away?");
                if(HumanTake=="1"):
                    return 0;
                elif(HumanTake=="2"):
                    return 1;
                else:
                    print("Please input 1 or 2!");


#Function do_move()
#args:
#       direction: 0->move left , 1->move right
#       player: 0->computer , 1->human
#return:
#       No return
def do_move(direction,player):
    global CurrentIndex,GameTree;
    if(direction==1):
        CurrentIndex = 2*CurrentIndex+2;
        if(player==0):
            print("Computer takes 2 away.",GameTree[CurrentIndex].value,"left.");
        else:
            print("Human player takes 2 away.",GameTree[CurrentIndex].value,"left.");
    elif(direction==0):
        CurrentIndex = 2*CurrentIndex+1;
        if(player==0):
            print("Computer takes 1 away.",GameTree[CurrentIndex].value,"left.");
        else:
            print("Human player takes 1 away.",GameTree[CurrentIndex].value,"left.");

#solve function
def solve(init_pos,primitive,generate_moves,do_move):
    global GameTree,CurrentIndex,CurrentPlayer;
    GameTree[CurrentIndex].primitive = primitive(CurrentIndex,GameTree[CurrentIndex].value,GameTree[CurrentIndex].primitive,CurrentPlayer);
    Movement = generate_moves(GameTree[CurrentIndex].primitive,CurrentIndex,CurrentPlayer);
    do_move(Movement,CurrentPlayer);

#initial settings
            
# Game "n-0" , where n=GameNumber
CurrentIndex = 0;
GameNumber = 0;
numberstr = input("What number of n do you want to choose when playing 'n-0'");
GameNumber = int(numberstr);

#generate a game tree
GameTree = [];
for i in range(pow(2,GameNumber+1)-1):
    GameTree.append(Node(0,GameNumber,0,-1));
GameTree[0].primitive = 2;

#who plays first
ComputerFirst = 0;
TypeinCorrect = 0;
while(TypeinCorrect == 0):
    FirstPlayer = input("Who plays first? Please type in 'Computer' or 'Human':");
    if(FirstPlayer == "Computer"):
        CurrentPlayer = 0;
        TypeinCorrect = 1;
        ComputerFirst = 0;
    elif(FirstPlayer == "Human"):
        CurrentPlayer = 1;
        TypeinCorrect = 1;
        ComputerFirst = 1;
    else:
        print("Please type in a correct word. 'Computer' or 'Human'?");


#Game Starts!!

while(GameTree[CurrentIndex].value>0):
    #GameTree[CurrentIndex].primitive = primitive(CurrentIndex,GameTree[CurrentIndex].value,GameTree[CurrentIndex].primitive,CurrentPlayer);
    #Movement = generate_moves(GameTree[CurrentIndex].primitive,CurrentIndex,CurrentPlayer);
    #do_move(Movement,CurrentPlayer);
    solve(CurrentIndex,primitive,generate_moves,do_move);
    CurrentPlayer = (CurrentPlayer+1)%2;
#if(ComputerFirst == 0):
if(CurrentPlayer==0):
    print("Human player wins! Congratulations!");
else:
    print("Computer beats you.");

#The End.
print("The end of the game");

# test function
#for i in range(pow(2,GameNumber+1)-1):
#    print('index',i,GameTree[i].primitive,'len2root',GameTree[i].len2leaf);
