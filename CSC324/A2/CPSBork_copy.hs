{-|
Module: CPSBork Assignment 2
Description: Continuation Passing Style Transformations
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

* Before starting, please review the exercise guidelines at
http://www.cs.toronto.edu/~lczhang/324/homework.html *

-}
-- This lists what this module exports. Don't change this!

module CPSBork (
    -- Warmup
    cpsFacEnv, fibEnv, cpsFibEnv,
    -- CPS Transform
    cpsDef, cpsExpr
) where

import qualified Data.Map as Map
import Test.QuickCheck (quickCheck)
import Ex10Bork (Env, emptyEnv, Value(..), HaskellProc(..), Expr(..), eval, def)

------------------------------------------------------------------------------
-- Warmup
------------------------------------------------------------------------------

-- | facEnv is an environment containing the function `fac` that computes the 
--   factorial of a number, written in direct style.
facEnv :: Env
facEnv = def [("fac", Lambda ["n"]
                (If (Equal (Var "n") (Literal $ Num 0))
                    (Literal $ Num 1)
                    (Times (Var "n") (App (Var "fac")
                       [(Plus (Var "n") (Literal $ Num (-1)))]))))]

-- | cpsFacEnv is an environment containing the function `cps_fac` that computes the 
--   factorial of a number, written in CPS
cpsFacEnv :: Env
cpsFacEnv = def [("cps_fac", Lambda ["n","k"]
                (If (Equal (Var "n") (Literal $ Num 0))
                    --apply function k to number 1
                    (App (Var "k") [Literal $ Num 1])
                    --else
                    (App (Var "cps_fac") [(Plus (Var "n") (Literal $ Num (-1))), 
                      (Lambda ["res"] (App (Var "k") [(Times (Var "n") (Var "res"))]))])))]


-- | fibEnv is an environment containing the function `fib` that computes the 
--   n-th fibonacci via recursion, written in direct style.
fibEnv :: Env
fibEnv = def [("fib", Lambda ["n"]
                (If (Equal (Var "n") (Literal $ Num 0))
                    (Literal $ Num 0)
                      (If (Equal (Var "n") (Literal $ Num 1))
                        (Literal $ Num 1)
                        (Plus (App (Var "fib") [(Plus (Var "n") (Literal $ Num (-1)))])
                               (App (Var "fib") [(Plus (Var "n") (Literal $ Num (-2)))])))))]

-- | cpsFfibEnv is an environment containing the function `fib` that computes the 
--   n-th fibonacci via recursion, written in direct style.
cpsFibEnv :: Env
cpsFibEnv = def [("cps_fib", Lambda ["n","k"]
                (If (Equal (Var "n") (Literal $ Num 0))
                  --apply function k to number 0
                    (App (Var "k") [Literal $ Num 0])
                    (If (Equal (Var "n") (Literal $ Num 1))
                      --apply function k to number 1
                        (App (Var "k") [Literal $ Num 1])
                        --recursion
                        (App (Var "cps_fib") [(Plus (Var "n") (Literal $ Num (-1))),
                          (Lambda ["num1"] (App (Var "cps_fib") [(Plus (Var "n") (Literal $ Num (-2))),
                            (Lambda ["num2"] (App (Var "k") [(Plus (Var "num1") (Var "num2"))]))]))]))))]

-- | An identity function in Bork, used for testing
identityFn :: Expr
identityFn = Lambda ["x"] (Var "x")

-- | Some simple tests. You should write your own.

prop_testFac :: Bool
prop_testFac = eval facEnv (App (Var "fac") [Literal $ Num 3]) == Num 6
prop_testCpsFac :: Bool
prop_testCpsFac = eval cpsFacEnv (App (Var "cps_fac") [Literal $ Num 3, identityFn]) == Num 6

prop_testFib :: Bool
prop_testFib = eval fibEnv (App (Var "fib") [Literal $ Num 6]) == Num 8

prop_testCpsFib :: Bool
prop_testCpsFib = eval cpsFibEnv (App (Var "cps_fib") [Literal $ Num 6, identityFn]) == Num 8
------------------------------------------------------------------------------
-- CPS Transformation
------------------------------------------------------------------------------

-- | Performs CPS Transformations on a list of name -> expression bindings
-- by renaming the names, and CPS transforming the expressions
cpsDef :: [(String, Expr)] -> [(String, Expr)]
cpsDef bindings = map (\(s, e) -> (rename s, cpsExpr e "" id)) bindings 

-- | CPS Transform a single expression
cpsExpr :: Expr -> String -> (Expr -> Expr) -> Expr
-- literals:
cpsExpr (Literal v) s context = context (Literal v)
-- variables:
cpsExpr (Var name) s context = context (Var (rename name))
-- builtins:
cpsExpr (Plus left right) s context = cpsExpr left "left_plus_" (\cpsLeft -> 
                                                      cpsExpr right "right_plus_" (\cpsRight -> 
                                                        context (Plus cpsLeft cpsRight)))

cpsExpr (Times left right) s context = cpsExpr left "left_times_" (\cpsLeft -> 
                                                      cpsExpr right "right_times_" (\cpsRight -> 
                                                        context (Times cpsLeft cpsRight)))

cpsExpr (Equal left right) s context = cpsExpr left "left_equal_" (\cpsLeft -> 
                                                      cpsExpr right "right_equal_" (\cpsRight -> 
                                                        context (Equal cpsLeft cpsRight)))
-- function definition:
cpsExpr (Lambda params body) s context = let newparams = ((map rename params) ++ ["k"]) 
                                         in cpsExpr body "lambda_" (\cps_body -> context (Lambda newparams (App (Var "k") [cps_body])))


-- function application: App Expr [Expr]  
--with exactly 1 argument
cpsExpr (App fn [arg]) s context = cpsExpr fn s (\func-> cpsExpr arg s 
                                                 (\arg1-> (App func [arg1, (Lambda [s++"result"] (context (Var (s++"result"))))])))
-- function application:  
--with exactly 2 arguments
cpsExpr (App fn [param1,param2]) s context = cpsExpr fn s (\func-> cpsExpr param1 s
                                                 (\arg1-> cpsExpr param2 s
                                                 (\arg2-> (App func [arg1, arg2, (Lambda [s++"result"] (context (Var (s++"result"))))]))))

-- function application:  
--with exactly 3 arguments
cpsExpr (App fn [param1,param2,param3]) s context = cpsExpr fn s (\func-> cpsExpr param1 s 
                                                 (\arg1-> cpsExpr param2 s 
                                                 (\arg2-> cpsExpr param3 s 
                                                 (\arg3-> (App func [arg1, arg2,arg3,(Lambda [s++"result"] (context (Var (s++"result"))))])))))

-- function application:  
--with exactly 4 arguments
cpsExpr (App fn [param1,param2,param3,param4]) s context = cpsExpr fn s (\func-> cpsExpr param1 s 
                                                 (\arg1-> cpsExpr param2 s 
                                                 (\arg2-> cpsExpr param3 s 
                                                 (\arg3-> cpsExpr param4 s 
                                                 (\arg4-> (App func [arg1, arg2,arg3,arg4,(Lambda [s++"result"] (context (Var (s++"result"))))]))))))

-- function application:  
--with exactly 5 arguments
cpsExpr (App fn [param1,param2,param3,param4,param5]) s context = cpsExpr fn s (\func-> cpsExpr param1 s 
                                                 (\arg1-> cpsExpr param2 s 
                                                 (\arg2-> cpsExpr param3 s 
                                                 (\arg3-> cpsExpr param4 s 
                                                 (\arg4-> cpsExpr param5 s 
                                                 (\arg5-> (App func [arg1,arg2,arg3,arg4,arg5,(Lambda [s++"result"] (context (Var (s++"result"))))])))))))

-- if expressions
cpsExpr (If cond conseq altern) s context = undefined

-- | Helper function that renames a variable by prepending "cps_"
rename :: String -> String
rename s = "cps_" ++ s

--------------------------------------------------------------------
-- | Some simple tests. You should also write your own.
--------------------------------------------------------------------

prop_testCpsExprLiteral :: Bool
prop_testCpsExprLiteral = result == Num 1
    where bindings = cpsDef [("n", Literal $ Num 1)]
          env = def bindings
          result = eval env $ Var ("cps_n")

prop_testCpsExprVar :: Bool
prop_testCpsExprVar = result == Num 2
    where bindings = cpsDef [("n", Literal $ Num 2),
                             ("m", Var "n")]
          env = def bindings
          result = eval env $ Var ("cps_m")

prop_testCpsExprPlus :: Bool
prop_testCpsExprPlus = result == Num 5
    where bindings = cpsDef [("n", Literal $ Num 2),
                             ("m", (Plus (Var "n") (Literal $ Num 3)))]
          env = def bindings
          result = eval env $ Var "cps_m"

prop_testCpsExprTimes :: Bool
prop_testCpsExprTimes = result == Num 24
    where bindings = cpsDef [("n", Literal $ Num 4),
                             ("m", (Times (Var "n") (Literal $ Num 6)))]
          env = def bindings
          result = eval env $ Var "cps_m"

prop_testCpsExprEqual :: Bool
prop_testCpsExprEqual = result == T
    where bindings = cpsDef [("n", Literal $ Num 4),
                             ("m", (Equal (Var "n") (Literal $ Num 4)))]
          env = def bindings
          result = eval env $ Var "cps_m"

prop_testCpsExprFac :: Bool
prop_testCpsExprFac = result == Num 120
    where bindings = cpsDef [("fac", Lambda ["n"]
                                (If (Equal (Var "n") (Literal $ Num 0))
                                    (Literal $ Num 1)
                                    (Times (Var "n") (App (Var "fac")
                                       [(Plus (Var "n") (Literal $ Num (-1)))]))))]
          env = def bindings
          result = eval env $ (App (Var "cps_fac") [Literal $ Num 5, identityFn])

--Test cases for function application
prop_testCpsExprTwoParam :: Bool
prop_testCpsExprTwoParam = result == T
    where bindings = cpsDef [("f", (Lambda ["x", "y"] (Plus (Var "x") (Var "y")))),
                             ("t", (App (Var "f") [Literal $ Num 5, Literal $ Num 7])),
                             ("m", (Equal (Var "t") (Literal $ Num 12)))]
          env = def bindings
          result = eval env $ Var "cps_m"

prop_testCpsExprFiveParam :: Bool
prop_testCpsExprFiveParam = result == T
    where bindings = cpsDef [("f", (Lambda ["a", "b","c","d","e"] (Plus (Var "e") (Times (Plus (Var "a") (Var "b")) (Plus (Var "c") (Var "d")))))),
                             ("t", (App (Var "f") [Literal $ Num 1, Literal $ Num 2,Literal $ Num 3,Literal $ Num 4,Literal $ Num 5])),
                             ("m", (Equal (Var "t") (Literal $ Num 26)))]
          env = def bindings
          result = eval env $ Var "cps_m"

--Test cases for prefix
--f x = (h x) + (j x) 
prop_testCpsExprPrefix :: Bool
prop_testCpsExprPrefix = result == Num 36
    where bindings = cpsDef [("h", (Lambda ["x"] (Plus (Var "x") (Literal $ Num 10)))),
                             ("j", (Lambda ["x"] (Plus (Var "x") (Literal $ Num 20)))),
                             ("f", (Lambda ["x"] (Plus (App (Var "h") [Var "x"]) (App (Var "j") [Var "x"])))),
                             ("m", (App (Var "f") [Literal $ Num 3]))]
          env = def bindings
          result = eval env $ Var "cps_m"

--wierd example
--prop_testCpsExprTest :: Bool
--prop_testCpsExprTest = result == Lambda ["cps_x", "cps_y", "k"] (App (Var "cps_f") [Var "cps_x", Lambda ["result"] (App (Var "k") [Var "result"])])
--    where result = cpsExpr (Lambda ["x", "y"] (App (Var "f") [(Var "x")])) "" id

------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

-- | This main function runs the quickcheck tests.
-- This gets executed when you compile and run this program. We'll talk about
-- "do" notation much later in the course, but for now if you want to add your
-- own tests, just define them above, and add a new `quickcheck` line here.
main :: IO ()
main = do
    --passed tests:
    --quickCheck prop_testFac
    --quickCheck prop_testCpsFac
    --quickCheck prop_testCpsExprLiteral 
    --quickCheck prop_testCpsExprVar 
    --quickCheck prop_testCpsExprPlus
    --quickCheck prop_testCpsExprTimes
    --quickCheck prop_testCpsExprEqual
    --quickCheck prop_testFib
    --quickCheck prop_testCpsFib
    --quickCheck prop_testCpsExprTwoParam
    --quickCheck prop_testCpsExprFiveParam

    --can't be ran yet
    --quickCheck prop_testCpsExprFac 
    quickCheck prop_testCpsExprPrefix

