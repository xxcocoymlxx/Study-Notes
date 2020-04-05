{- CSC324 Fall 2018 Lab 9 -}

module Lab9 where

-- |
-- = Task 1: Fitting some generic functions
-- For each of the functions below, give an implementation
-- of them so that they are *total* (always terminate and don't raise
-- and error), and compile with the given type signatures.

-- Feel free to change the function and parameter names to be more descriptive!


-- Note that (_, _) is the Haskell *tuple* type, which is also generically polymorphic.
f0 :: int -> (int, int)
f0 x = (x,x)

--f1 takes 3 parameters, a function,its args a, b, and returns c
--note: f1 and myFunc return the same thing!
f1 :: (a -> b -> c) -> a -> b -> c
f1 myFunc x y = (myFunc x y)

--f2 takes 3 arguments, 2 functions and returns c
--note: myFunc2's return value is muFunc1's imput
f2 :: (b -> c) -> (a -> b) -> a -> c
f2 myFunc1 myFunc2 x = (myFunc1 (myFunc2 x))

-- What's special about this one?
-- return a function
f3 :: (a, b) -> (c -> b)
f3 (x, y) = \c -> y


-- |
-- = Task 2: One new generic type, `Maybe`

-- For your reference, here's the definition of the `Maybe` type built into Haskell:
-- data Maybe = Nothing | Just a

safeHead :: [a] -> Maybe a
safeHead l = if null l
             then Nothing
             else Just (head l)

safeTail :: [a] -> Maybe [a]
safeTail l = if null l
             then Nothing
             else Just (tail l)

--which succeeds only when its second argument satisfies its first.
onlyWhen :: (a -> Bool) -> a -> Maybe a
onlyWhen f x = if (f x)
               then Just x
               else Nothing

-- There are only two possible total functions with this type signature. 
--Pick the one that isn’t a constant function. 
--Watch the brackets when doing pattern-matching!
try :: (a -> b) -> Maybe a -> Maybe b
try f Nothing = Nothing
try f (Just x) = Just (f x)


-- |
-- = Task 3: Introduction to typeclasses

data Shape
    = Circle Float            -- ^ A circle with the given radius
    | Rectangle Float Float   -- ^ A rectangle with the given width and height
    | Square Float            -- ^ A square with the given side length

instance Eq Shape where
    Circle a == Circle b = a == b
    Rectangle a b == Rectangle c d = a == c && b == d
    Square a == Square b = a == b
    Rectangle a b == Square c = a == b && b == c
    _ == _ = False
