{- CSC324 Fall 2019: Exercise 9

*Before starting, please review the exercise guidelines at
https://www.cs.toronto.edu/~lczhang/324/homework.html*
-}
module Ex9 (typeCheck) where

-- This is one of Haskell's built-in analogues of dictionaries.
-- You may want to read up on the available functions here:
-- https://hackage.haskell.org/package/containers-0.4.2.0/docs/Data-Map.html
import qualified Data.Map as Map

-- | Import the types used for this exercise
import Ex9Types (Type(..), Formula(..), TypeEnv, Formulas)

-- | Imports used for testing purposes only.
import Control.Monad (liftM, liftM2)
import Test.QuickCheck (
    Property, quickCheck, oneof, sized, Arbitrary(..)
    )

------------------------------------------------------------------------------
-- Example Formula from the handout
------------------------------------------------------------------------------

exampleTypeEnv :: TypeEnv
exampleTypeEnv = Map.fromList [
    ("first_name", StrCol),
    ("last_name", StrCol),
    ("full_name", StrCol)]

exampleFormulas :: Formulas
exampleFormulas = Map.fromList [
    ("first_name", Nothing),
    ("last_name", Nothing),
    ("full_name", Just (Concat (Column "first_name") (Column "last_name")))]

------------------------------------------------------------------------------
-- Task 1: Type Checking
------------------------------------------------------------------------------

-- | This is the core type-checking function.
--
-- We recommend using the `Map.foldlWithKey` function to iterate through
-- one of the Maps, and using `typeCheckFormula` as a helper function
-- to check each of the columns
--you won't be able to use the typeCheckFormula function directly as 
--the first argument to a foldlWithKey because the types won't match up.
 
--You may assume that the two arguments to typeCheck contain 
--the same set of keys (same column names). 
--如果对应column没有formula，就pass
--如果有formula，就check formula return的value type是否等于TypeEnv里define的type

--1. You can create a helper function that uses pattern matching with "Nothing" and "Just <type>".
--2. You can use "case ... of" syntax, as demonstrated in other questions on Piazza.
typeCheck :: TypeEnv -> Formulas -> Bool
typeCheck tenv fs = Map.foldlWithKey (\result k v -> case v of
                               Just formula  -> result && (typeCheckFormula formula (convert (Map.lookup k tenv)) tenv)
                               Nothing -> True) True fs


convert :: Maybe a -> a
convert (Just a) = a


-- | Helper function to check if a particular formula matches its type by:
--      * Checking if the formula return type matches the actual return type
--      * Checking if the formula's argument type matches what is in the TypeEnv
-- This helper function is not tested. You are welcome to use a different
-- implementation strategy and create your own helper functions.
typeCheckFormula :: Formula -> Type -> TypeEnv -> Bool
typeCheckFormula (Column a) returnType typeEnv = convert (Map.lookup a typeEnv) == returnType

typeCheckFormula (Plus a b) returnType typeEnv = (typeCheckFormula a NumCol typeEnv) && 
                                                 (typeCheckFormula b NumCol typeEnv) &&
                                                 (returnType == NumCol)

typeCheckFormula (Concat a b) returnType typeEnv = (typeCheckFormula a StrCol typeEnv) && 
                                                 (typeCheckFormula b StrCol typeEnv) &&
                                                 (returnType == StrCol)

typeCheckFormula (Length a) returnType typeEnv = (typeCheckFormula a StrCol typeEnv) && (returnType == NumCol)

typeCheckFormula (NumToString a) returnType typeEnv = (typeCheckFormula a NumCol typeEnv) && (returnType == StrCol)


------------------------------------------------------------------------------
-- Sample Tests
------------------------------------------------------------------------------

prop_testTypeCheckFormula :: Bool
prop_testTypeCheckFormula = (typeCheckFormula (Length (Column "a"))
                                              NumCol
                                              (Map.fromList [("a", StrCol)]))

prop_testExamplePass :: Bool
prop_testExamplePass = typeCheck exampleTypeEnv exampleFormulas

prop_testExample2Fail :: Bool
prop_testExample2Fail = False == (typeCheck exampleTypeEnv2 exampleFormulas2)
    where exampleTypeEnv2 = Map.fromList [("a", StrCol),
                                          ("b", StrCol)]
          exampleFormulas2 = Map.fromList [("a", Nothing),
                                           ("b", Just (Length (Column "a")))]
prop_testExample3Pass :: Bool
prop_testExample3Pass = (typeCheck exampleTypeEnv3 exampleFormulas3)
    where exampleTypeEnv3 = Map.fromList [("a", StrCol),
                                          ("b", StrCol)]
          exampleFormulas3 = Map.fromList [("a", Nothing),
                                           ("b", Just (NumToString (Length (Column "a"))))]

-- This main function runs the quickcheck tests.
-- This gets executed when you compile and run this program. We'll talk about
-- "do" notation later in the course, but for now if you want to add your
-- own tests, just define them above, and add a new `quickcheck` line here.
main :: IO ()
main = do
    -- | uncomment if you are implementing the typeCheckFormula helper:
    quickCheck prop_testTypeCheckFormula
    quickCheck prop_testExamplePass 
    quickCheck prop_testExample2Fail
    quickCheck prop_testExample3Pass

