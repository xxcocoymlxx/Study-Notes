{-|
Module: Ex9Types
Description: Types for Exercise 9
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

This module provides the public types required for Exercise 9.
You should review the data types in this file carefully, but do not
change anything in this file! We will use a fresh copy of this file
for testing purposes.
-}

module Ex9Types (Type(..), Formula(..), TypeEnv, Formulas) where

-- This is one of Haskell's built-in analogues of dictionaries.
-- You may want to read up on the available functions here:
-- https://hackage.haskell.org/package/containers-0.4.2.0/docs/Data-Map.html
import qualified Data.Map as Map


------------------------------------------------------------------------------
-- Data Definitions (don't change these)
------------------------------------------------------------------------------

data Type = NumCol | StrCol
          deriving (Eq, Show)

data Formula = Column String           -- :: a -> a (could be NumCol or StrCol)
             | Plus   Formula Formula  -- :: NumCol -> NumCol -> NumCol
             | Concat Formula Formula  -- :: StrCol -> StrCol -> StrCol
             | Length Formula          -- :: StrCol -> NumCol
             | NumToString Formula     -- :: NumCol -> StrCol
            deriving (Eq, Show)

--a dictionary with key: string (column name) and 
--value: Type(data type of the column)
type TypeEnv = Map.Map String Type
--a dictionary with key: string (column name) and 
--value: Formula (how this column is calculated)
type Formulas = Map.Map String (Maybe Formula)

