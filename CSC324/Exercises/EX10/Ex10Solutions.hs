{-|
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
--import Test.QuickCheck (quickCheck)
import Ex10Types (Env, emptyEnv, Value(..), HaskellProc(..), Expr(..))

------------------------------------------------------------------------------
-- * Task 1. CPS Transforming Haskell Functions *
------------------------------------------------------------------------------

-- | Compute the factorial of a number
-- factorial :: Int -> Int

-- | Compute the factorial of a number, in continuation passing style
cpsFactorial:: Int -> (Int -> r) -> r
cpsFactorial 0 k = k 1
cpsFactorial n k = 
    cpsFactorial (n-1) $ \fval -> k (n * fval)

-- | Compute the n-th fibonacci number F(n).
--    Recall F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2)
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = (fib (n - 1)) + (fib (n - 2))

-- | Compute the n-th fibonacci number F(n), in continuation passing style
cpsFibonacci:: Int -> (Int -> r) -> r
cpsFibonacci 0 k = k 0
cpsFibonacci 1 k = k 1
cpsFibonacci n k = 
    cpsFibonacci (n-1) $ \f1 ->
    cpsFibonacci (n-2) $ \f2 ->
        k (f1 + f2)

-- | Sample tests:
prop_testFactorial :: Bool
prop_testFactorial = (cpsFactorial 3 id) == 6
prop_testFibonacci :: Bool
prop_testFibonacci = (cpsFibonacci 6 id) == 8

------------------------------------------------------------------------------
-- | List functions

myLength :: [a] -> Int
myLength []     = 0
myLength (x:xs) = 1 + myLength xs


-- | CPS transform of the function `length`, which computes the length of a list
cpsLength :: [a] -> (Int -> r) -> r
cpsLength []     k = k 0
cpsLength (x:xs) k = cpsLength xs $ \n -> k $ n+1


-- | CPS transform of the function `map`. The argument function (to be applied
--   every element of the list) is written in direct style
cpsMap :: (a -> b) -> [a] -> ([b] -> r) -> r
cpsMap f []     k = k []
cpsMap f (x:xs) k = cpsMap f xs $ \rest -> k (f(x):rest)

-- | Sample tests:
prop_cpsLength :: Bool
prop_cpsLength = (cpsLength [1,2,3] id) == 3
prop_cpsMap :: Bool
prop_cpsMap = (cpsMap (2*) [1,2,3,4,5] id) == [2,4,6,8,10]

------------------------------------------------------------------------------
-- Merge Sort

-- | Sort a list using mergeSort
mergeSort :: [Int] -> [Int]
mergeSort []  = []
mergeSort [x] = [x]
mergeSort lst = let (xs, ys) = split lst
    in merge (mergeSort xs) (mergeSort ys)

-- | Split a list into two lists. All list elements in even indices
-- is placed in one sub-list, and all list elements in odd indicies
-- is placed in the second sub-list.
split :: [Int] -> ([Int], [Int])
split [] = ([], [])
split (x:[]) = ([x], [])
split (x:y:rest) = let (xs, ys) = split rest
    in ((x:xs), (y:ys))

-- | Merge two sorted lists together
merge :: [Int] -> [Int] -> [Int]
merge x [] = x
merge [] y = y
merge (x:xs) (y:ys) = if x < y
    then x:(merge xs (y:ys))
    else y:(merge (x:xs) ys)

-- | CPS transform of mergeSort
cpsMergeSort :: [Int] -> ([Int] -> r) -> r
cpsMergeSort []  k = k []
cpsMergeSort [x] k = k [x]
cpsMergeSort lst k = 
    cpsSplit lst $ \(xs, ys) ->
    cpsMergeSort xs $ \sortedXs ->
    cpsMergeSort ys $ \sortedYs ->
    cpsMerge sortedXs sortedYs $ \merged ->
    k merged

-- | CPS transform of split
cpsSplit :: [Int] -> (([Int], [Int]) -> r) -> r
cpsSplit []     k = k ([], [])
cpsSplit (x:[]) k = k ([x], [])
cpsSplit (x:y:rest) k =
    cpsSplit rest $ \(xs, ys) -> k ((x:xs), (y:ys))

-- | CPS transform of merge
cpsMerge :: [Int] -> [Int] -> ([Int] -> r) -> r
cpsMerge x [] k = k x
cpsMerge [] y k = k y
cpsMerge (x:xs) (y:ys) k = if x < y
    then cpsMerge xs (y:ys) $ \merged -> k (x:merged)
    else cpsMerge (x:xs) ys $ \merged -> k (y:merged)

-- | Sample tests:
prop_cpsMergeSort :: Bool
prop_cpsMergeSort = (cpsMergeSort [1,2,4,3] id) == [1,2,3,4]

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
cpsEval env (Plus a b) k =
    cpsEval env a $ \va ->
    cpsEval env b $ \vb ->
        case (va, vb) of
            (Num x, Num y) -> k $ Num (x + y)
            _              -> Error "plus"
cpsEval env (Times a b) k =
    cpsEval env a $ \va ->
    cpsEval env b $ \vb ->
        case (va, vb) of
            (Num x, Num y) -> k $ Num (x * y)
            _              -> Error "times"
cpsEval env (Equal a b) k =
    cpsEval env a $ \va ->
    cpsEval env b $ \vb ->
        if va == vb then k T else k F
cpsEval env (Var name) k =
    case (Map.lookup name env) of
        Just a  -> k a
        Nothing -> Error "lookup"
cpsEval env (Lambda params body) k = k $ Procedure $ Proc (\values k2 ->
    let newEnv = Map.union (Map.fromList (zip params values)) env
    in cpsEval newEnv body k2)

cpsEval env (If cond t f) k =
    cpsEval env cond $ \vc ->
        if vc == T then cpsEval env t k else cpsEval env f k


cpsEval env (App proc args) k =
    cpsEval env proc $ \vproc ->
    cpsArg  env args [] $ \vargs -> -- call helper
        case vproc of
            Procedure (Proc fn) -> fn vargs k
            _ -> Error "app"

            
cpsEval env (Shift name body) k =
    let newEnv = (Map.insert name (Procedure (Proc (\[v] c -> c $ k v))) env)
    in cpsEval newEnv body id
cpsEval env (Reset body) k =
    case cpsEval env body id of
        Error v -> Error v
        v       -> k v

-- helper function
cpsArg env []         vargs k = k (reverse vargs)
cpsArg env (arg:args) vargs k =
    cpsEval env arg $ \varg -> cpsArg env args (varg:vargs) k



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

prop_cpsEvalExample1 :: Bool
prop_cpsEvalExample1 = example1 == Num 3
prop_cpsEvalExample2 :: Bool
prop_cpsEvalExample2 = example2 == Num 12
prop_cpsEvalExample3 :: Bool
prop_cpsEvalExample3 = example3 == T

out = (cpsEval emptyEnv
                    (Plus (Literal $ Num 5)
                    (Plus (Literal $ Num 3) 
                        (Shift "d" 
                            (Plus 
                                (App (Var "d") [Literal $ Num 5]) 
                                (App (Var "d") [Literal $ Num 6]))
                    )))
                    id) 

------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

-- | This main function runs the quickcheck tests.
-- This gets executed when you compile and run this program. We'll talk about
-- "do" notation much later in the course, but for now if you want to add your
-- own tests, just define them above, and add a new `quickcheck` line here.
