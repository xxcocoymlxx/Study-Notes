#lang racket #| CSC324 Fall 2019: Exercise 2 |#
#|
* Before starting, please review the exercise guidelines at
http://www.cs.toronto.edu/~lczhang/324/homework.html *
|#
;-------------------------------------------------------------------------------
; This expression exports functions so they can be imported into other files.
; Don't change it!
(provide calculate tail-calls)

;-------------------------------------------------------------------------------
; * Task 1: Calculator II *
;-------------------------------------------------------------------------------

(define/match (calculate expr)
  [((list '+ a b)) (+ (calculate a) (calculate b))]
  [((list '- a b)) (- (calculate a) (calculate b))]
  [((list '* a b)) (* (calculate a) (calculate b))]
  [((list '/ a b)) (/ (calculate a) (calculate b))]
  [((list 'if (list '= a b) c d)) (if (equal? (calculate a) (calculate b)) (calculate c) (calculate d))]
  [((list 'if (list '> a b) c d)) (if (> (calculate a) (calculate b)) (calculate c) (calculate d))]
  [((list 'if (list '< a b) c d)) (if (< (calculate a) (calculate b)) (calculate c) (calculate d))]
  [(_) (if (number? expr) expr (calculate expr))]
  )

(module+ test
  (require rackunit)
  ; Please add additional test cases
  (test-equal? "Simple if statement"
               (calculate '(if (= 0 1) 4 5))
               5)
  (test-equal? "Nested if statement"
               (calculate '(+ 1 (if (= 0 1) 4 5)))
               6)
  (test-equal? "comparing expressions"
               (calculate '(+ 1 (if (= (+ 0 0) (+ 3 1)) 4 5)))
               6)
  (test-equal? "no single numbers, all expressions"
               (calculate '(+ 1 (if (= (* 10 0) (+ 65 1)) (+ 2 4) (+ 5 2))))
               8)
    (test-equal? "most complex, nested if expressions"
               (calculate '(+ 1 (if (= (* 10 0) (+ 65 1)) (if (= 0 1) 4 5) (if (= 0 1) 4 9))))
               10))

;-------------------------------------------------------------------------------
; * Task 2: Detecting tail calls *
;-------------------------------------------------------------------------------

#|
(tail-calls expr)
  expr: A racket datum with the structure defined on the exercise handout.

  Returns a *list of function call expressions* that are in tail call position
  with respect to the input expression.

  Feel free to change the define into define/match to use pattern-matching instead!
|#
(define (tail-calls expr)
  (tail-calls-help expr '()))


(define/match (tail-calls-help expr acc)
  ;1st pattern, the "and" situation
  [((cons 'and exprs) acc)
   (if (equal? exprs '())
       acc
       (append acc (tail-calls-help (last exprs) '())))]

  ;2nd pattern, the "or" situation
  [((cons 'or exprs) acc)
   (if (equal? exprs '())
       acc
       (append acc (tail-calls-help (last exprs) '())))]

  ;3rd pattern, (if <cond> <then> <else>)
  [((cons 'if (cons cond-expr (cons then-expr (cons else-expr '())))) acc)
   (append (append acc (tail-calls-help then-expr '())) (tail-calls-help else-expr '()))]

  ;4th pattern, (function <expr> <expr> ...)
  ;if None of its subexpressions are in tail call position, then it's a function call that in tail position
  [((cons proc-expr exprs) acc)
   (let* ([all-expr-result (map (lambda (x) (tail-calls-help x '())) exprs)];get all return result from every sub-expression
          [all-tail (filter (lambda (y) (not (equal? y '()))) all-expr-result)];remove all the empty list from all-expr-result
          [is-tail (> (length all-expr-result) (length all-tail))]);if it's true, means its a function in tail position
     (if is-tail
         (append acc (list (cons proc-expr exprs)))
         (append acc all-tail)))]
  
  ;5th patter, an atomic value
  [(_ acc) acc])

(module+ test
  (require rackunit)
  ; We've provided test cases for the first three syntactic forms described
  ; in the handout. Please add additional test cases, including ones for the
  ; other forms!
  (test-equal? "Atomic value" (tail-calls 3) empty)
  (test-equal? "Simple call" (tail-calls '(+ 1 2)) (list '(+ 1 2)))
  (test-equal? "Nested call"
               (tail-calls '(+ (* 3 4) 2))
               ; NOTE: the outermost expression is in tail-call position,
               ; and it should just be output directly. Don't try to evaluate
               ; the inner '(* 3 4) -- this is harder to do!
               (list '(+ (* 3 4) 2)))
  (test-equal? "Simple if" (tail-calls '(if (> x 0) (- x 2) (+ x 3)))
               (list '(- x 2)
                     '(+ x 3))))
