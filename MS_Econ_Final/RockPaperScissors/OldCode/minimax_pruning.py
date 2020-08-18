# Python3 program to demonstrate  
# working of Alpha-Beta Pruning  
  
# Initial values of Aplha and Beta  
MAX, MIN = 1000, -1000 
  
# Returns optimal value for current player  
#(Initially called for root and maximizer)  
def minimax(depth, nodeIndex, maximizingPlayer,  
            values, alpha, beta):  
   
    # Terminating condition. i.e  
    # leaf node is reached  
    if depth == 3:  
        return values[nodeIndex]  
  
    if maximizingPlayer:  
       
        best = MIN 
  
        # Recur for left and right children  
        for i in range(0, 64):  # changed 2 -> 64 
              
            val = minimax(depth + 1, nodeIndex * 2 + i,  
                          False, values, alpha, beta)  
            best = max(best, val)  
            alpha = max(alpha, best)  
  
            # Alpha Beta Pruning  
            if beta <= alpha:  
                break 
           
        return best  
       
    else: 
        best = MAX 
  
        # Recur for left and  
        # right children  
        for i in range(0, 64):  # changed 2 -> 64
           
            val = minimax(depth + 1, nodeIndex * 2 + i,  
                            True, values, alpha, beta)  
            best = min(best, val)  
            beta = min(beta, best)  
  
            # Alpha Beta Pruning  
            if beta <= alpha:  
                break 
           
        return best  
       
# Driver Code  
if __name__ == "__main__":  
   
    values = ScoreA  
    print("The optimal value is :", minimax(0, 0, True, values, MIN, MAX))  
      
# This code is contributed by Rituraj Jain 
# source: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

# should sort by the type of weight then make into a list
# ScoreA = games.groupby('weights_A', as_index=False)['ScoreA'].to_list()
    # it is already grouped by weights_A
ScoreA = games['ScoreA'].to_list()

games[games['ScoreA']==794.0]

