{-|
Module: Ex6
Description: Exercise 6: More OOP, and Haskell!
Copyright: (c) University of Toronto, 2019
               CSC324 Principles of Programming Languages, Fall 2019

* Before starting, please review the exercise guidelines at
http://www.cs.toronto.edu/~lczhang/324/homework.html *

This part of the exercise is similar in spirit to Exercise 1, except using
the Haskell programming language instead.

The one /new/ idea here is the use of the QuickCheck library to use a different
kind of approach to testing called /property-based testing/. We illustrate a
few simple property-based tests throughout this file.
-}

-- This lists what this module exports. Don't change this!
module Ex6
  (
  -- Task 2
    celsiusToFahrenheit
  , nCopies
  , numEvens
  , numManyEvens
  , calculate
  -- Task 3
  , expressionsOfRank
  , arithmeticExpressions
  )
where

-- You *may* add imports from Data.List for task 3 (but no other imports).
import Data.List (sort)
import Test.QuickCheck (Property, quickCheck, (==>))
import Ex6Types (Expr(..))

-------------------------------------------------------------------------------
-- |
-- * Task 2: Working with Haskell
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- * Note about type signatures
--
-- Unlike Racket, Haskell is /statically-typed/. We'll go into more detail about
-- what this means later in the course, but for now we've provided type signatures
-- for the functions here to simplify any compiler error messages you might
-- receive. (Don't change them; they're required to compile against our tests.)
-------------------------------------------------------------------------------

-- | Converts a temperature from Celsius to Fahrenheit.
-- __Note__: use the @round@ function to convert from floating-point types
-- to @Int@.
celsiusToFahrenheit :: Float -> Int
celsiusToFahrenheit temp =
    -- TODO: replace `undefined` with a proper function body.
    round(32 + (temp * 1.8))
    --done

-- | The simplest "property-based test" is simply a unit test; note the type.
prop_celsius0 :: Bool
prop_celsius0 = celsiusToFahrenheit 0 == 32
prop_celsius37 :: Bool
prop_celsius37 = celsiusToFahrenheit 37 == 99

-------------------------------------------------------------------------------
-- * Recursion with numbers
--
-- For the recursive functions, we recommend doing these in two ways:
--
--   1. First, write them using @if@ expressions, as you would in Racket.
--   2. Then when that works, use /pattern-matching/ to simplify the definitions
--      (<http://learnyouahaskell.com/syntax-in-functions#pattern-matching>).
--
-- Remember: Strings are simply lists of characters. (@String === [Char]@)
-- Read more about manipulating lists at
-- <http://learnyouahaskell.com/starting-out#an-intro-to-lists>.

-- | Returns a new string that contains @n@ copies of the input string.
nCopies :: String -> Int -> String
nCopies s 0 = ""
nCopies s n = s ++ nCopies s (n - 1)
--done


-- | This is a QuickCheck property that says,
-- "If n >= 0, then when you call nCopies on a string s and int n,
-- the length of the resulting string is equal to
-- n * the length of the original string."
--
-- QuickCheck verifies this property holds for a random selection of
-- inputs (by default, choosing 100 different inputs).
prop_nCopiesLength :: String -> Int -> Property
prop_nCopiesLength s n = n >= 0 ==> length (nCopies s n) == (length s * n)

-------------------------------------------------------------------------------
-- * Recursion with lists
-------------------------------------------------------------------------------

-- | Returns the number of even elements in the given list.
--
-- We've given you a pattern matching template here to start from.
numEvens :: [Int] -> Int
numEvens [] = 0            -- base case
numEvens (x:[]) = if even x then 1 else 0
numEvens (first:rest) = (numEvens [first]) + (numEvens rest)  -- recursive case
--done

-- | Returns the number of inner lists that contain three or more even integers.
numManyEvens :: [[Int]] -> Int
numManyEvens [] = 0
numManyEvens [x] = if (numEvens x) > 2 then 1 else 0
numManyEvens (x:xs) = (numManyEvens [x]) + (numManyEvens xs)
--done


-- | This is a property that says, "the number returned by numEvens is
-- less than or equal to the length of the original list."
prop_numEvensLength :: [Int] -> Bool
prop_numEvensLength nums = numEvens nums <= length nums

-- | What do you think this property says?
prop_numManyEvensDoubled :: [[Int]] -> Bool
prop_numManyEvensDoubled listsOfNums =
  let doubled = listsOfNums ++ listsOfNums
  in numManyEvens doubled == 2 * (numManyEvens listsOfNums)

-------------------------------------------------------------------------------
-- * The Haskell Calculator
-------------------------------------------------------------------------------

-- | calculate: take an Expr, and evaluate it to return a number
-- Here you'll need to use pattern-matching on the different forms of an Expr 
-- (@Number@ or @Add@ or @Sub@ ...), because we don't have an explicit "number?"
-- function for this datatype.
calculate :: Expr -> Float
calculate (Number n) = n
    -- In this case, the expression is a number

calculate (Add expr1 expr2) = (calculate expr1) + (calculate expr2)
    -- In this case, the expression is an addition

calculate (Sub expr1 expr2) = (calculate expr1) - (calculate expr2)
    -- In this case, the expression is a subtraction

calculate (Mul expr1 expr2) = (calculate expr1) * (calculate expr2)
    -- In this case, the expression is a multiplication

calculate (Div expr1 expr2) = (calculate expr1) / (calculate expr2)
    -- In this case, the expression is a division


-------------------------------------------------------------------------------
-- | This property checks that (calculate expr) is always one less than
-- | than (calculate (Add (Number 1) expr))
prop_calculateAdd :: Expr -> Bool
prop_calculateAdd expr = ((calculate expr) + 1) == (calculate (Add (Number 1) expr))

-- | What do you think this property says?
prop_calculateSub:: Expr -> Bool
prop_calculateSub expr = ((calculate expr) - 1) == (calculate (Sub expr (Number 1)))

-- | What do you think this property says?
prop_calculateDouble:: Expr -> Bool
prop_calculateDouble expr = ((calculate expr) * 2) == (calculate (Mul (Number 2) expr))

-- | What do you think this property says?
prop_calculateHalf :: Expr -> Bool
prop_calculateHalf expr = ((calculate expr) / 2) == (calculate (Div expr (Number 2)))

-------------------------------------------------------------------------------
-- |
-- * Task 3: Generating Expressions
-------------------------------------------------------------------------------

numbers :: [Expr]
numbers = [Number 1, Number 2, Number 3, Number 4] 

makeAdd :: Expr -> Expr -> Expr
makeAdd a b = Add a b

makeMul :: Expr -> Expr -> Expr
makeMul a b = Mul a b

-- | Returns a list of Expr *of rank k* that uses numbers 1-4, Add, and Mul.
-- grammar from the exercise handout. The expressions can be in any order.
-- Order matters in an expression (so `(+ 3 4)` is different from `(+ 4 3)`),
-- and no expression should appear twice in the output list.
--
-- Precondition: k >= 0.
--
-- Hints:
--   1. The only expressions at rank 0 are the numeric literals in the list `numbers`:
--         Number 1, Number 2, Number 3, Number 4
--   2. This function can (and probably should) be recursive!
--   3. Remember that you aren't *evaluating* any expressions here.
--      Don't get distracted trying to "evaluate" "(+ 3 4)" into "7".
--   4. Make helper function(s)! This function is quite elegant if you do some
--      design work to think about what helper(s) you really need here.
--   5. Spend some time reading through the Haskell List documentation
--      to get some ideas about the functions you might find useful.
--      https://hackage.haskell.org/package/base-4.10.1.0/docs/Data-List.html
--      In particular, concatMap is pretty sweet. :)
--
--      Along the same lines, http://learnyouahaskell.com/starting-out#texas-ranges.
--      (Note: [0..(-1)] is an empty list.)

--Function 1
expressionsOfRank :: Int -> [Expr]
--base case
--a list of Expr of rank 0
expressionsOfRank 0 = numbers

--base case
--a list of Expr of rank 1
expressionsOfRank 1 = allCombinations numbers numbers

-- think about how to divide up the “expressions of rank k” into
-- mutually exclusive sets of expressions,
-- generate each set separately, and then combine them in the end.
-- the two mutually exclusive sets are: "expressionsUpToRank" and "expressionsOfRank"
--note: order matters, to get different result with the same list, we swap the order of them
expressionsOfRank n = (allCombinations (expressionsUpToRank (n - 1)) (expressionsOfRank (n - 1)))
                      ++
                      (allCombinations (expressionsOfRank (n - 1)) (expressionsUpToRank (n - 1)))

-------------------------------------------
--Function 2
-- | An infinite list containing all arithmetic expressions (again, no duplicates),
-- in *non-decreasing rank order*. Expressions of the same rank may appear in any order.
arithmeticExpressions :: [Expr]
arithmeticExpressions = concatMap (\k -> expressionsOfRank k) [0..]

-------------------------------------------------------------------------------
--helper functions (4 in total)

--1
--Now, we fix the element n, and do combination of it with elements in lst
--to operate ADD and MUL
--"++" means to append two lists
combinations n lst = (map (\x -> makeAdd n x) lst) ++ (map (\x -> makeMul n x) lst)

--2
--Now, we fix the elements in lst2, and do combination of it with elements in lst1
allCombinations lst1 lst2 = concatMap (\x -> combinations x lst2) lst1

--3
--get a list of all exprs with rank up to n
expressionsUpToRank n = expressionsUpToRankHelper n numbers

--4
--tail recursion helper to expressionsUpToRank
--each time we append expression of rank (n), (n-1), (n-2)...to the accumulator
expressionsUpToRankHelper 0 acc = acc
expressionsUpToRankHelper n acc = expressionsUpToRankHelper (n - 1) (acc ++ (expressionsOfRank n))

-------------------------------------------------------------------------------
-- | Exact test for rank 0 expressions.
prop_arithRank0Exact :: Bool
prop_arithRank0Exact =
    sort (expressionsOfRank 0) == numbers

-- | Test for number of rank 1 expressions.
prop_arithRank1Length :: Bool
prop_arithRank1Length =
    length (sort (expressionsOfRank 1)) == 2 * (length numbers) * (length numbers)

-- | Most naive implementations will miss this. Be careful here!
-- Also, see the note on the handout about efficiency.
prop_arithRank3ElemCheck :: Bool
prop_arithRank3ElemCheck =
    elem (Add (Mul (Add (Number 3)  (Number 2)) (Number 4)) (Number 1)) (expressionsOfRank 3)


-------------------------------------------------------------------------------
-- * Main function (for testing purposes only)
-------------------------------------------------------------------------------

-- This main function is executed when you compile and run this Haskell file.
-- It runs the QuickCheck tests; we'll talk about "do" notation much later in
-- the course, but for now if you want to add your own tests, just define them
-- above, and add a new `quickCheck` line below.
main :: IO ()
main = do
  quickCheck prop_celsius0
  quickCheck prop_celsius37
  quickCheck prop_nCopiesLength
  quickCheck prop_numEvensLength
  quickCheck prop_numManyEvensDoubled
  quickCheck prop_calculateAdd
  quickCheck prop_calculateSub
  quickCheck prop_calculateDouble
  quickCheck prop_calculateHalf
  quickCheck prop_arithRank0Exact
  quickCheck prop_arithRank1Length
  quickCheck prop_arithRank3ElemCheck

