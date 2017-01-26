int,acc:int,arr[]:int,i:int;
(if (eq (length arr) i) acc (bsd (accumulator acc (get arr i)) arr (add i 1)))