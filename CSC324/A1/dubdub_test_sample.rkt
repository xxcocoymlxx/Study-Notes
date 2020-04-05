#lang racket #| * CSC324 Fall 2019: Assignment 1 Sample Tests * |#
#|
Module: dubdub_test_sample
Description: Sample Tests for Assignment 1
Copyright: (c) University of Toronto, University of Toronto Mississauga
               CSC324 Principles of Programming Languages, Fall 2019

Warning: as usual, these sample tests are very incomplete, and are meant to
give you a sense of the test structure we'll use, but NOT to verify the
complete correctness of your work on this assignment! Please add your own
tests here
|#

(require rackunit)
(require "dubdub.rkt")
(require "dubdub_errors.rkt")


(module+ test
  (test-equal? "Numeric literal"
                 (run-interpreter '(30))
                 30)

  (test-equal? "Multiple independent defines"
                 (run-interpreter '((define a 1)
                                    (define b #t)
                                    (define c #f)
                                    b))
                 #t)

  (test-exn "Identifier with unused define (unbound-name error)"
              (regexp (format (hash-ref error-strings 'unbound-name) 'b))
              (thunk (run-interpreter '((define a 10)
                                        b))))

  (test-equal? "Simple +"
                 (run-interpreter '((+ 30 40)))
                 70)

  (test-equal? "Unary function call"
                 (run-interpreter '(((lambda (x) (+ x 1)) 1)))
                 2)

  (test-equal? "make-adder (curried)"
                 (run-interpreter '((define make-adder (lambda (n m) (+ n m)))
                                    (define add-one (make-adder 1))
                                    (define add-two (make-adder 2))
                                    (+ (add-one 5) (add-two 10))))
                 ; We write out explicitly the computation produced using
                 ; correct substitution.
                 (+ (+ 1 5) (+ 2 10)))

  (test-equal? "Contract: (integer? -> boolean?), valid call"
                 (run-interpreter '((define-contract f (integer? -> boolean?))
                                    (define f (lambda (x) (< x 3)))
                                    (f 1)))
                 #t)
  
  (test-equal? "Contract: (integer? integer? -> boolean?), valid curried call"
                 (run-interpreter '((define-contract f (integer? integer? -> boolean?))
                                    (define f (lambda (x y) (< x 3)))
                                    (define g (f 1))
                                    (g 1)))
                 #t)
  
  (test-equal? "Contract: (integer? integer? -> any?) with any"
                 (run-interpreter '((define-contract f (integer? any -> any))
                                    (define f (lambda (x y) (< x 3)))
                                    (define g (f 1))
                                    (g 1)))
                 #t)

  (test-equal? "two defines of function"
                 (run-interpreter '((define f (lambda (x) (+ x 1)))
                                    (define g (lambda () f))
                                    ((g) 5)))
                 6)


 (test-equal? "procedure?"
                 (run-interpreter '((procedure? (+ 1 2))))
                 #f)

  
  (test-equal? "procedure?"
                 (run-interpreter '((procedure? (lambda () (+ 1 3)))))
                 #t)
  
 (test-equal? "procedure?"
                 (run-interpreter '((define a (lambda () (+ 1 3)))
                                    (procedure? a)))
                 #t)
  
 (test-equal? "procedure?"
                 (run-interpreter '((define a (lambda () (+ 1 3)))
                                    (define b a)
                                    (procedure? b)))
                 #t)

 (test-equal? "Name Shadowing"
                 ;(take lst pos) get an error if pos > (length lst)
                 (run-interpreter '((define a 4)
                                    (define b (lambda (a) (+ a 2)))
                                    (b 1)))
                 3)
  (test-equal? "Name Shadowing"
                 ;(take lst pos) get an error if pos > (length lst)
                 (run-interpreter '((define a 3) (integer? a)))
                 #t)

  (test-exn "error: contract-violation error (curried)"
              (regexp (hash-ref error-strings 'contract-violation))
              (thunk (run-interpreter '((define-contract f (boolean? integer? -> boolean?))
                                    (define f (lambda (x y) (< x 3)))
                                    (define g (f 1))
                                    (g 1)))))

  (test-exn "error: contract-violation error (non-curried)"
              (regexp (hash-ref error-strings 'contract-violation))
              (thunk (run-interpreter '((define-contract f (boolean? -> boolean?))
                                    (define f (lambda (x) (< x 3)))
                                    (f 1)))))
  
  (test-exn "error: duplicate-name"
              (regexp (format (hash-ref error-strings 'duplicate-name) 'x))
              (thunk (run-interpreter '( (define f (lambda (x x) (+ x 1))) 2))))
  
  (test-exn "error: duplicate-name"
              (regexp (format (hash-ref error-strings 'duplicate-name) 'f))
              (thunk (run-interpreter '( (define f (lambda (x) (+ x 1))) (define f 1)))))

  (test-exn "error: arity-mismatch"
              (regexp (format (hash-ref error-strings 'arity-mismatch) 2 1))
              (thunk (run-interpreter '(((lambda (x) (+ x 6)) 5 6)))))

  (test-exn "error: invalid contract"
              (regexp (format (hash-ref error-strings 'invalid-contract) 'f2))
              (thunk (run-interpreter '((define-contract f2 ((lambda (x) (< 10 x)) (lambda (x) (< 0 x)) -> (lambda (x) (< 0 x))))
                      (define f2 (lambda (x) (+ x 2)))(f2 12)))))

  (test-exn "error: not a function"
              (regexp (format (hash-ref error-strings 'not-a-function) 'f))
              (thunk (run-interpreter '((define-contract f (integer? -> boolean?)) (f 3 4)))))


  (test-equal? "contract: with functions"
              (run-interpreter '((define-contract f2 ((lambda (x) (< 0 x)) (lambda (x) (< 0 x)) -> (lambda (x) (< 0 x))))
                                    (define f2 (lambda (x y) (+ x y)))
                                    (f2 1 2)))
              3)
  
  (test-exn "error: contract violation"
              (regexp (hash-ref error-strings 'contract-violation))
              (thunk (run-interpreter '((define-contract f2 ((lambda (x) (< 5 x)) (lambda (x) (< 0 x)) -> (lambda (x) (< 0 x))))
                                    (define f2 (lambda (x y) (+ x y)))
                                    (f2 1 2)))))
  
  (test-exn "error: invalid contract, a function has two contracts"
              (regexp (format (hash-ref error-strings 'invalid-contract) 'f2))
              (thunk (run-interpreter '((define-contract f2 ((lambda (x) (< 5 x)) (lambda (x) (< 0 x)) -> (lambda (x) (< 0 x))))
                                        (define-contract f2 ((lambda (x) (< 5 x)) (lambda (x) (< 0 x)) -> (lambda (x) (< 0 x))))
                                    (define f2 (lambda (x y) (+ x y)))
                                    (f2 1 2)))))
#|
case1:
Since add-one expects 2 arguments (m and z), I think the error should be:
ERROR: function called with an incorrect number of arguments. Given: 3, Expected: 2

(run-interpreter '((define make-adder (lambda (n m z) (+ n m)))
                                    (define add-one (make-adder 1))
                                    (define add-two (make-adder 2 3))
                                    (+ (add-one 5 1 3) (add-two 10))))


case2:
(run-interpreter '(((lambda (x) (x 5 6)) +)))

|#

  )
