#!/usr/bin/env python3
"""Ant Colony Optimization for TSP."""
import random, math, sys

class ACO:
    def __init__(self, dists, n_ants=20, alpha=1, beta=2, rho=0.5, Q=100):
        self.dists=dists; self.n=len(dists); self.n_ants=n_ants
        self.alpha=alpha; self.beta=beta; self.rho=rho; self.Q=Q
        self.pheromone=[[1.0]*self.n for _ in range(self.n)]
    def _tour(self):
        start=random.randrange(self.n); visited={start}; tour=[start]
        while len(tour)<self.n:
            cur=tour[-1]; probs=[]
            for j in range(self.n):
                if j not in visited and self.dists[cur][j]>0:
                    p=self.pheromone[cur][j]**self.alpha*(1/self.dists[cur][j])**self.beta
                    probs.append((j,p))
            if not probs: break
            total=sum(p for _,p in probs); r=random.random()*total; cum=0
            for j,p in probs:
                cum+=p
                if cum>=r: tour.append(j); visited.add(j); break
        return tour
    def _length(self, tour):
        return sum(self.dists[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour)))
    def solve(self, iterations=50):
        best=None; best_len=float('inf')
        for it in range(iterations):
            tours=[self._tour() for _ in range(self.n_ants)]
            for i in range(self.n):
                for j in range(self.n): self.pheromone[i][j]*=(1-self.rho)
            for tour in tours:
                L=self._length(tour)
                if L<best_len: best=tour; best_len=L
                for i in range(len(tour)):
                    a,b=tour[i],tour[(i+1)%len(tour)]
                    self.pheromone[a][b]+=self.Q/L
            if it%(iterations//5)==0: print(f"Iter {it}: best={best_len:.1f}")
        return best, best_len

if __name__ == "__main__":
    random.seed(42); n=8
    cities=[(random.uniform(0,100),random.uniform(0,100)) for _ in range(n)]
    dists=[[math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) for b in cities] for a in cities]
    tour,length=ACO(dists).solve(100)
    print(f"Tour: {tour}, Length: {length:.1f}")
