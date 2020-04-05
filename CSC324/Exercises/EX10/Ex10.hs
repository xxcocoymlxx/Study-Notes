
\{-|
Module: Ex10
Description: Exercise 10: Continuation Passing Style
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

* Before starting, please review the exercise guidelines at
http://www.cs.toronto.edu/~lczhang/324/homework.html *

-}
-- This lists what this module exports. Don't change this!

module Ex10 (
    -- Task 1
    cpsFactorial, cpsFibonacci, cpsLength, cpsMap,
    cpsMergeSort, cpsSplit, cpsMerge,
    -- Task 2
    cpsEval
) where

import qualified Data.Map as Map
import Test.QuickCheck (quickCheck)
import Ex10Types (Env, emptyEnv, Value(..), HaskellProc(..), Expr(..))

------------------------------------------------------------------------------
-- * Task 1. CPS Transforming Haskell Functions *
------------------------------------------------------------------------------

-- | Compute the factorial of a number
-- factorial :: Int -> Int

-- | Compute the factorial of a number, in continuation passing style
--in Haskell, the expression a $ b c is equivalent to a (b c)
cpsFactorial:: Int -> (Int -> r) -> r
cpsFactorial 0 k = k 1
cpsFactorial n k = cpsFactorial (n-1) (\res -> k (n * res))

-- | Compute the n-th fibonacci number F(n).
--    Recall F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2)
-- fibonacci :: Int -> Int

-- | Compute the n-th fibonacci number F(n), in continuation passing style
cpsFibonacci:: Int -> (Int -> r) -> r
cpsFibonacci 0 k = k 0
cpsFibonacci 1 k = k 1
cpsFibonacci n k = (cpsFibonacci (n - 1) (\a -> cpsFibonacci (n - 2) (\b -> (k (a + b))))) 

-- | Sample tests:
prop_testFactorial :: Bool
prop_testFactorial = (cpsFactorial 3 id) == 6
prop_testFibonacci :: Bool
prop_testFibonacci = (cpsFibonacci 6 id) == 8

------------------------------------------------------------------------------
-- | List functions

-- | CPS transform of the function `length`, which computes the length of a list
cpsLength :: [a] -> (Int -> r) -> r
cpsLength [] k = k 0
cpsLength (x:xs) k = (cpsLength xs (\result -> k (1 + result)))

-- | CPS transform of the function `map`. The argument function (to be applied
--   every element of the list) is written in direct style
cpsMap :: (a -> b) -> [a] -> ([b] -> r) -> r
cpsMap f [] k = k []
cpsMap f (x:xs) k = (cpsMap f xs (\result -> k ((f x):result)))

-- | Sample tests:
prop_cpsLength :: Bool
prop_cpsLength = (cpsLength [1,2,3] id) == 3
prop_cpsMap :: Bool
prop_cpsMap = (cpsMap (2*) [1,2,3,4,5] id) == [2,4,6,8,10]

------------------------------------------------------------------------------
-- Merge Sort

-- | Sort a list using mergeSort
-- mergeSort :: [Int] -> [Int]

-- | Split a list into two lists. All list elements in even indices
-- is placed in one sub-list, and all list elements in odd indicies
-- is placed in the second sub-list.
-- split :: [Int] -> ([Int], [Int])

-- | Merge two sorted lists together
-- merge :: [Int] -> [Int] -> [Int]


-- | CPS transform of split
cpsSplit :: [Int] -> (([Int], [Int]) -> r) -> r
cpsSplit [] k = k ([], [])
--you have to have this case, otherwise it doesnt handle the case of odd elements
--and will raise an error: non-exaustive pattern
cpsSplit [x] k = k ([x], [])
--remenber All elements in even indices
-- is placed in first sub-list, and all elements in odd indicies
-- is placed in the second sub-list.
-- you have to specify the indexes, otherwise it will be infinite recursion!!!
cpsSplit (x:y:xs) k = (cpsSplit xs (\(lst1,lst2) -> k (x:lst1,y:lst2)))

-- | CPS transform of merge
cpsMerge :: [Int] -> [Int] -> ([Int] -> r) -> r
cpsMerge lst1 [] k = k lst1
cpsMerge [] lst2 k = k lst2
cpsMerge (l:ls) (r:rs) k = if l < r 
                           then (cpsMerge ls (r:rs) (\result -> k (l:result)))
                           else (cpsMerge (l:ls) rs (\result -> k (r:result)))


-- | CPS transform of mergeSort
cpsMergeSort :: [Int] -> ([Int] -> r) -> r
cpsMergeSort [] k = k []
cpsMergeSort [x] k = k [x]
cpsMergeSort lst k = (cpsSplit lst (\(lst1,lst2) -> cpsMergeSort lst1 (\leftsorted-> cpsMergeSort lst2 (\rightsorted-> cpsMerge leftsorted rightsorted (\res -> k res)))))



-- | Sample test: even number of elements
prop_cpsMergeSort :: Bool
prop_cpsMergeSort = (cpsMergeSort [1,2,4,3] id) == [1,2,3,4]
 
-- | Sample test: odd number of elements
prop_cpsMergeSort1 :: Bool
prop_cpsMergeSort1 = (cpsMergeSort [9,8,7,6,5,4,3,2,1] id) == [1,2,3,4,5,6,7,8,9]

------------------------------------------------------------------------------
-- * Task 2. CPS Transforming The Bork Interpreter *
------------------------------------------------------------------------------

-- | A CPS interpreter `eval` for Bork, which takes an environment,
--   an expression, and a continuation, and calls the continuation with
--   the evaluated value.
--   Notice that the type signature of `eval` is less general compared to
--   usual, i.e. it is not:
--      Env -> Expr -> (Value -> r) -> r
--   This restriction on the type of the continuation makes it easier
--   to errors.
cpsEval :: Env -> Expr -> (Value -> Value) -> Value
cpsEval env (Literal v) k = k v

cpsEval env (Plus a b) k = case ((cpsEval env a k), (cpsEval env b k)) of
    (Num x, Num y) -> k $ Num (x + y)
    _              -> Error "plus"

cpsEval env (Times a b) k = case ((cpsEval env a k), (cpsEval env b k)) of
    (Num x, Num y) -> k $ Num (x * y)
    (c, d)         -> Error "times"

cpsEval env (Equal a b) k = if (cpsEval env a k) == (cpsEval env b k) then k T else k F

cpsEval env (Var name) k = case (Map.lookup name env) of
    Just a  -> k a
    Nothing -> Error "lookup"

cpsEval env (If cond expr alt) k = if (cpsEval env cond k) == T
    then (cpsEval env expr (\res -> k res))
    else (cpsEval env alt (\res -> k res))

--too tricky, and don't think you'll really learn much by figuring this one out
cpsEval env (Lambda params body) k = k $ Procedure $ Proc (\values k2 ->
    let newEnv = Map.union (Map.fromList (zip params values)) env
    in cpsEval newEnv body k2)


--------------------------------------------------------------------------------
--The general case of app which takes more than 2 parameters
cpsEval env (App proc args) k = cpsEval env proc (\res -> case res of
    Procedure (Proc f) -> f (helper env args k) k
    _                  -> Error "app")


helper :: Env -> [Expr] -> (Value -> Value) -> [Value]
helper env args k = map (\arg -> cpsEval env arg k) args

--------------------------------------------------------------------------------


------------------------------------------------------------------------------
-- Example Bork Programs (CPS)
------------------------------------------------------------------------------

-- | Example: apply the identity function to the number 3
example1 = cpsEval emptyEnv (App (Lambda ["a"] (Var "a")) [Literal $ Num 3]) id

-- | Example: apply a function that returns 10 plus the second argument
--            to the arguments [1, 2]
example2 = cpsEval emptyEnv (App (Lambda ["a", "b"] (Plus (Literal $ Num 10) (Var "b")))
                              [Literal $ Num 1, Literal $ Num 2]) id
-- | Example: if statement expression
example3 = cpsEval emptyEnv (If (Equal (Literal F) (Literal F))
                             (Literal T)
                             (Literal F)) id
example4 = cpsEval emptyEnv (App (Lambda ["x"] (Plus (Var "x") (Literal (Num 2)))) [Literal (Num 3)]) id

example5 = cpsEval emptyEnv (App (Lambda ["x", "y", "z"] (Times (Var "x") (Var "y"))) [(Literal (Num 3)), (Literal (Num 4)), (Literal (Num 5))]) id


-- | Example: recursive case
example6 = cpsEval emptyEnv (If (Equal (App (Lambda ["x", "y", "z"] (Times (Var "x") (Var "y"))) [(Literal (Num 3)), (Literal (Num 4)), (Literal (Num 5))])
                                (Literal (Num 12)))
                             (Literal T)
                             (Literal F)) id


-- | Example: recursive case2
example7 = cpsEval emptyEnv (If (Equal (App (Lambda ["x", "y", "z"] (Times (Var "x") (Var "y"))) [(Literal (Num 3)), (Literal (Num 4)), (Literal (Num 5))])
                                (Literal (Num 7)))
                             (Literal T)
                             (Literal F)) id

prop_cpsEvalExample1 :: Bool
prop_cpsEvalExample1 = example1 == Num 3
prop_cpsEvalExample2 :: Bool
prop_cpsEvalExample2 = example2 == Num 12
prop_cpsEvalExample3 :: Bool
prop_cpsEvalExample3 = example3 == T
prop_cpsEvalExample4 :: Bool
prop_cpsEvalExample4 = example4 == Num 5
prop_cpsEvalExample5 :: Bool
prop_cpsEvalExample5 = example5 == Num 12

prop_cpsEvalExample6 :: Bool
prop_cpsEvalExample6 = example6 == T

prop_cpsEvalExample7 :: Bool
prop_cpsEvalExample7 = example7 == F


------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

-- | This main function runs the quickcheck tests.
-- This gets executed when you compile and run this program. We'll talk about
-- "do" notation much later in the course, but for now if you want to add your
-- own tests, just define them above, and add a new `quickcheck` line here.
main :: IO ()
main = do
    --quickCheck prop_testFactorial
    --quickCheck prop_testFibonacci 
    --quickCheck prop_cpsLength
    --quickCheck prop_cpsMap
    --quickCheck prop_cpsMergeSort
    --quickCheck prop_cpsMergeSort1
    --quickCheck prop_cpsEvalExample1
    --quickCheck prop_cpsEvalExample2
    --quickCheck prop_cpsEvalExample3
    --quickCheck prop_cpsEvalExample4
    --quickCheck prop_cpsEvalExample5
      quickCheck prop_cpsEvalExample6
      quickCheck prop_cpsEvalExample7
