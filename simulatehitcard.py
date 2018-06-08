import random
import itertools
import math
import pickle
import sys
import numpy as np

def EvalHand(pair):
  count = 0
  for card in pair:
    if card == 'A':
      count += 11
    else:
      count += int(card)
  return count

def Simulate(upcard, pcard1, pcard2):
  over10 = [str(10) for i in range(16)]
  lower10 = [str(i) for i in range(2,10) for j in range(4)]
  ace = ['A' for i in range(4)]

  deck = list()
  deck.extend(over10)
  deck.extend(lower10)
  deck.extend(ace)

  deck.pop(deck.index(upcard))
  deck.pop(deck.index(pcard1))
  deck.pop(deck.index(pcard2))

  resulteachhit = {}
  for hitcard in ['2','3','4','5','6','7','8','9','10','A']:
    result = {}
    result[17] = 0
    result[18] = 0
    result[19] = 0
    result[20] = 0
    result[21] = 0
    result['burst'] = 0
    loopdeck = deck.copy()
    loopdeck.pop(loopdeck.index(hitcard))
    for i in range(100000):
      tmpdeck = loopdeck.copy()
      random.shuffle(tmpdeck)

      hand = [upcard]
      while EvalHand(hand) < 17:
        hand.append(tmpdeck.pop())
  
      score = EvalHand(hand)
      if score > 21:
        result['burst'] += 1
      else:
        result[score] += 1

    #print(hitcard, result)
    resulteachhit[hitcard] = result.copy()

  return resulteachhit

def main():
  if len(sys.argv) < 4:
    sys.exit()
  
  upcard = sys.argv[1]
  pcard1 = sys.argv[2]
  pcard2 = sys.argv[3]

  resulteachhit = Simulate(upcard, pcard1, pcard2)

  resultM = np.zeros((10,6))
  for i,hitcard in enumerate(['2','3','4','5','6','7','8','9','10','A']):
    for j,num in enumerate([17,18,19,20,21,'burst']):
      resultM[i,j] = resulteachhit[hitcard][num]

  p = np.array([4,4,4,4,4,4,4,4,16,4])
  for card in [upcard, pcard1, pcard2]:
    if card == 'A':
      p[9] -= 1
    else:
      p[int(card)-2] -= 1
  p = p / 49.0
  M = np.reshape(p, (10,1)) * resultM
  result = np.round(np.sum(M, axis=0)/1000, 2)

  output = [upcard,pcard1,pcard2]
  output.extend(list(map(str, list(result))))
  print(','.join(output))

if __name__ == '__main__':
  main()


