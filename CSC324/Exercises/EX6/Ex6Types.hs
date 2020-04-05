{-|
Module: Ex6Types
Description: Types for Exercise 6
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

This module provides the public types required for the Haskell portion of
Exercise 6. You should review the data type Expr carefully, but do not
change anything in this file! We will use a fresh copy of this file
for testing purposes.
-}
module Ex6Types
    ( Expr(..)
    )
where

import Control.Monad (liftM2)
import Test.QuickCheck (oneof, listOf1, sized, scale, Arbitrary(..), Gen, suchThat)


-------------------------------------------------------------------------------
-- * Task 2 (Expr type)
-------------------------------------------------------------------------------

data Expr = Number Float    -- ^ numeric literal
          | Add Expr Expr   -- ^ addition
          | Sub Expr Expr   -- ^ subtraction
          | Mul Expr Expr   -- ^ multiplication
          | Div Expr Expr   -- ^ division
          deriving (Show, Eq, Ord)

-- | Example: The number 20.
numberExample :: Expr
numberExample = Number 20

-- | Example: (+ 2 3)
addExample :: Expr
addExample = Add (Number 2) (Number 3)

-- | Example: (+ 2 (- 5 1))
exprExample :: Expr
exprExample = Add (Number 2) (Sub (Number 5) (Number 1))

-------------------------------------------------------------------------------
-- * Testing helpers
-- (You can safely ignore ALL of the code below. We don't expect you to
-- understand it at this point.)
-------------------------------------------------------------------------------

-- | Specify how to generate a "random" Expr
-- excluding the number 0 to avoid zero division
instance Arbitrary Expr where
    arbitrary = sized expr'
      where
        expr' 0 = oneof
            [ fmap Number (arbitrary :: Gen Float) `suchThat` (/= (Number 0))
            ]
        expr' n = scale (`div` 2) $ oneof
            [
              liftM2 Add arbitrary arbitrary
            , liftM2 Sub arbitrary arbitrary
            , liftM2 Mul arbitrary arbitrary
            , liftM2 Div arbitrary arbitrary
            ]
