#!/usr/bin/env python3
"""Ant colony optimization — solve TSP with pheromone trails."""
import random,math
def aco_tsp(dist,n_ants=20,iterations=100,alpha=1,beta=2,evaporation=0.5):
    n=len(dist);pheromone=[[1.0]*n for _ in range(n)]
    best_tour=None;best_len=float('inf')
    for _ in range(iterations):
        tours=[]
        for _ in range(n_ants):
            visited=[random.randint(0,n-1)];remaining=set(range(n))-{visited[0]}
            while remaining:
                cur=visited[-1]
                probs=[]
                for j in remaining:
                    tau=pheromone[cur][j]**alpha
                    eta=(1/dist[cur][j])**beta if dist[cur][j]>0 else 1e10
                    probs.append((j,tau*eta))
                total=sum(p for _,p in probs)
                r=random.random()*total;s=0
                for j,p in probs:
                    s+=p
                    if s>=r:visited.append(j);remaining.remove(j);break
            tours.append(visited)
        for tour in tours:
            length=sum(dist[tour[i]][tour[i+1]] for i in range(n-1))+dist[tour[-1]][tour[0]]
            if length<best_len:best_len=length;best_tour=tour
            for i in range(n):
                a,b=tour[i],tour[(i+1)%n]
                pheromone[a][b]+=1/length;pheromone[b][a]+=1/length
        for i in range(n):
            for j in range(n):pheromone[i][j]*=(1-evaporation)
    return best_tour,best_len
def main():
    random.seed(42)
    pts=[(random.random()*100,random.random()*100) for _ in range(10)]
    dist=[[math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) for b in pts] for a in pts]
    tour,length=aco_tsp(dist,n_ants=10,iterations=50)
    print(f"Tour length: {length:.2f}")
if __name__=="__main__":main()
