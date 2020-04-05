{- CSC324 Fall 2018 Lab 10 -}

module Lab10 where


-- |
-- = Task 1
mapMaybes :: (a -> b) -> [Maybe a] -> [Maybe b]
mapMaybes f [] = []-- base case: empty list
mapMaybes f (Nothing:xs) = Nothing:(mapMaybes f xs)
mapMaybes f ((Just v):xs) = (Just (f v)):(mapMaybes f xs)

composeMaybe :: (a -> Maybe b) -> (b -> Maybe c) -> (a -> Maybe c)
composeMaybe = undefined

foldMaybe :: (b -> a -> Maybe b) -> b -> [a] -> Maybe b
foldMaybe = undefined

applyBinaryMaybe :: (a -> b -> c) -> Maybe a -> Maybe b -> Maybe c
applyBinaryMaybe = undefined

collectMaybes :: [Maybe a] -> Maybe [a]
collectMaybes = undefined


