#!/bin/sh

for i in /data/python/flashcard/flashcard/*.pyc 
do
  rm $i && echo removed: $i
done

for i in /data/python/flashcard/flashcard/db/*.db 
do
  rm $i && echo removed: $i
done

