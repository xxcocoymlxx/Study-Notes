{-|
Module: Ex10Types
Description: Types for Exercise 6
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

This module provides the public types required for Task 2 of
Exercise 10. You should review the data type Expr carefully, but do not
change anything in this file! We will use a fresh copy of this file
for testing purposes.
-}

module Ex10Types (Env, emptyEnv, Value(..), HaskellProc(..), Expr(..)) where

import qualified Data.Map as Map

------------------------------------------------------------------------------
-- Data Definitions: the Bork language (CPS)
------------------------------------------------------------------------------

-- | An environment is a mapping of names to values
type Env = Map.Map String Value
emptyEnv = Map.empty

-- | Like before, Values in LambdEh include:
data Value = Nil | T | F            -- null values and booleans
           | Num Int                -- integers
           | Procedure HaskellProc  -- procedures (closures), see below
           | Error String           -- errors    
          deriving (Eq, Show)

-- | LambdEH procedures are represented using Haskell functions.
--   To complete the CPS transform, the procedures here also need
--   to be written in CPS.
data HaskellProc = Proc ([Value] -> (Value -> Value) -> Value)

instance Show HaskellProc where  
    show x = "[Can't Show Procedure]"
instance Eq HaskellProc where  
    x == y = False

-- | Expressions in LambdEh include:
data Expr = Literal Value           -- literal values
          | Plus Expr Expr          -- builtin "plus" function
          | Times Expr Expr         -- builtin "times" function
          | Equal Expr Expr         -- builtin checks for equality
          | Var String              -- variable names
          | If Expr Expr Expr       -- if statements
          | Lambda [String] Expr    -- function definitions
          | App Expr [Expr]         -- function applications
          | Shift String Expr       -- identical to `shift` in Racket
          | Reset Expr              -- identical to `reset` in Racket
          deriving (Eq, Show)

