{-|
Module: Ex10Bork
Description: Types for Exercise 6
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

This module contains the (non-CPS) version of the Bork interpreter, along
Do not write any of your solutions in this file.
-}
module Ex10Bork (
    Env, emptyEnv, Value(..), HaskellProc(..), Expr(..), eval, def
) where

import qualified Data.Map as Map

------------------------------------------------------------------------------
-- Data Definitions: the (non-CPS) Bork language
------------------------------------------------------------------------------

-- | An environment is a mapping of names to values
type Env = Map.Map String Value
emptyEnv = Map.empty

-- | Values in Bork include:
data Value = Nil | T | F            -- null values and booleans
           | Num Int                -- integers
           | Procedure HaskellProc  -- procedures (closures), see below
           | Error String           -- errors    
          deriving (Eq, Show)

-- | Bork procedures are represented using Haskell functions.
--   A procedure takes a list of arguments, and returns a single value.
--   This representation is different from the representations we used
--   in previous exercises and assignment, and is necessary for the CPS
--   transform in Part 3. We also define methods for comparing and
--   printing procedures.
data HaskellProc = Proc ([Value] -> Value)
instance Show HaskellProc where  
    show x = "[Can't Show Procedure]"
instance Eq HaskellProc where  
    x == y = False

-- | Expressions in Bork include:
data Expr = Literal Value           -- literal values
          | Plus Expr Expr          -- builtin "plus" function
          | Times Expr Expr         -- builtin "times" function
          | Equal Expr Expr         -- builtin checks for equality
          | Var String              -- variable names
          | If Expr Expr Expr       -- if statements
          | Lambda [String] Expr    -- function definitions
          | App Expr [Expr]         -- function applications
          deriving (Eq, Show)

------------------------------------------------------------------------------
-- Interpreter
------------------------------------------------------------------------------

-- | The interpreter `eval` for Bork, which takes an environment
--   and an expression, and returns the evaluated value.
eval :: Env -> Expr -> Value
eval env (Literal v) = v
eval env (Plus a b)  = case ((eval env a), (eval env b)) of
    (Num x, Num y) -> Num (x + y)
    _              -> Error "plus"
eval env (Times a b) = case ((eval env a), (eval env b)) of
    (Num x, Num y) -> Num (x * y)
    (c, d)         -> Error "times"
eval env (Equal a b) = if (eval env a) == (eval env b) then T else F
eval env (Var name)  = case (Map.lookup name env) of
    Just a  -> a
    Nothing -> Error "lookup"
eval env (If cond expr alt) = if (eval env cond) == T
    then (eval env expr)
    else (eval env alt)
eval env (Lambda params body) = Procedure $ Proc $ \vargs ->
    let newEnv = Map.union (Map.fromList (zip params vargs)) env
    in eval newEnv body
eval env (App proc args) = case (eval env proc) of
    Procedure (Proc f) ->  let vargs = (map (eval env) args)
                           in f vargs
    _                  -> Error "app"

------------------------------------------------------------------------------
-- Environment Definition
------------------------------------------------------------------------------

-- | Create a new environment from a set of bindings (pairs of names to
--   expressions to be evaluated). These expressions may be recursive:
--   in other words, the expression might reference names that are 
--   being defined. In order to support recursion, notice that we
--   are passing the `env` (currently being created) as the environment
--   in the call to `eval`! This is similar to how we use `letrec` in
--   Racket, but relies on Haskell's lazy evaluation.
def :: [(String, Expr)] -> Env
def bindings = 
    let env = Map.fromList (map (\(n,e) -> (n, (eval env e))) bindings)
    in env

------------------------------------------------------------------------------
-- Example Bork Programs
------------------------------------------------------------------------------

-- | Example: apply the identity function to the number 3
example1 = eval emptyEnv (App (Lambda ["a"] (Var "a")) [Literal $ Num 3])

-- | Example: apply a function that returns 10 plus the second argument
--            to the arguments [1, 2]
example2 = eval emptyEnv (App (Lambda ["a", "b"] (Plus (Literal $ Num 10) (Var "b")))
                              [Literal $ Num 1, Literal $ Num 2])
-- | Example: if statement expression
example3 = eval emptyEnv (If (Equal (Literal F) (Literal F))
                             (Literal T)
                             (Literal F))
-- | Example: creating a function using `def`
sub1Env = def [("sub1", Lambda ["n"] (Plus (Var "n") (Literal $ Num (-1))))]
example4 = eval sub1Env (App (Var "sub1") [Literal $ Num 5])

---- | Example: factorial
facEnv = def [("fac", Lambda ["n"]
                        (If (Equal (Var "n") (Literal $ Num 0))
                            (Literal $ Num 1)
                            (Times (Var "n") (App (Var "fac")
                               [(Plus (Var "n") (Literal $ Num (-1)))]))))]
example5 = eval facEnv (App (Var "fac") [Literal $ Num 5])

------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

-- main :: IO ()
-- main = do
--     print example1
--     print example2
--     print example3
--     print example4
--     print example5
