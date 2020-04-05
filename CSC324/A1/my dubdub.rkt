#lang racket
#| * CSC324 Fall 2019: Assignment 1 * |#
#|
Module: dubdub
Description: Assignment 1: A More Featureful Interpreter
Copyright: (c)University of Toronto, University of Toronto Mississauga 
               CSC324 Principles of Programming Languages, Fall 2019

The assignment handout can be found at

    https://www.cs.toronto.edu/~lczhang/324/files/a1.pdf

Please see the assignment guidelines at 

    https://www.cs.toronto.edu/~lczhang/324/homework.html
|#

(provide run-interpreter)

(require "dubdub_errors.rkt")


;-----------------------------------------------------------------------------------------
; Main functions (skeleton provided in starter code)
;-----------------------------------------------------------------------------------------
#|
(run-interpreter prog) -> any
  prog: datum?
    A syntactically-valid Dubdub program.

  Evaluates the Dubdub program and returns its value, or raises an error if the program is
  not semantically valid.
|#
(define (run-interpreter prog)
  (cond
    [(equal? 0 (length prog)) (void)] ;no prog
    [(equal? 1 (length prog)) (interpret (hash) (first prog))] ;only have <expr>
    [else
     (interpret (foldl (lambda (expr env) (interpret env expr)) (hash) (take prog (- (length prog) 1))) (last prog))];normal prog (<binding_or_contract> ... <expr>)
    ))


#|
(interpret env expr) -> any
  env: hash?
    The environment with which to evaluate the expression.
  expr: datum?
    A syntactically-valid Dubdub expression.

  Returns the value of the Dubdub expression under the given environment.
|#
(define (interpret env expr)
  (cond
    ;the expr is closure structrue
    [(closure? expr)
     (if (closure-slovable env expr)
         (if (equal? (list) (closure-contract expr)) (interpret env (closure-body expr));if no contract, return value
             (if (precond_check env expr)
                 (let ([result (interpret env (closure-body expr))])
                   (if (postcond_check expr result) result (report-error 'contract-violation)))
                 (report-error 'contract-violation)))
         (closure (closure-contract expr) env (closure-params expr) (closure-body expr)))] 

    [(number? expr) expr]                                                                                                                                    ;the expr is <expr> a number                   return expr

    [(boolean? expr) expr]                                                                                                                                    ;the expr is <expr> a boolean                  return expr

    [(builtin? expr) expr]
    
    [(symbol? expr)
     (if (hash-has-key? env expr) ;the expr is <expr> a symbol                   return Value / Error raised
         (hash-ref env expr)
         (report-error 'unbound-name expr))] 

    [(equal? (first expr) 'define) (env-update env (second expr) (interpret env (third expr)))]                                                                             ;the expr is <binding>                         return new env / Error raised

    [(equal? (first expr) 'define-contract)
     (if (check_contract (third expr));if the predicates are procedure or "any"
         (contract-update env (second expr) (third expr))
         (report-error 'invalid-contract (second expr)))]                                                                                     ;the expr is <contract>                        return new env

    [(equal? (first expr) 'lambda) (closure (list) env (second expr) (third expr))]                                                                                         ;the expr is <expr> function expresssion       Return Clousre

    [(builtin? (first expr))
     (apply (hash-ref builtins (first expr))                                                                                                  ;the epxr is a bulitin funciton call           Recursion
            (foldl (lambda (expr ls) (append ls (list (interpret env expr)))) (list) (rest expr)))] 

    [(equal? #f (or (builtin? (first expr)) (closure? (interpret env (first expr))))) (report-error 'not-a-function (first expr))]                                                                                          ;the expr is NOT A FUNCTION CALL,              Error raised


    [else
     (letrec ((clu (interpret env (first expr)))                                                                                              ;the expr is <expr> a function call            Recursion
              (arguments (foldl (lambda (exprsion results) (append results (list (interpret env exprsion)))) (list) (rest expr)))
              (unknow-parms (get-unknown-parms (closure-environment clu) (closure-params clu))))
       (cond
         [(> (length arguments) (length (closure-params clu)))
          (report-error 'arity-mismatch (length arguments) (length (closure-params clu)))]
                                                                                                                
         [(> (length arguments) (length unknow-parms))
          (interpret (foldl (lambda (k v environment) (hash-set environment k v))
                            (closure-environment clu)
                            (take (closure-params clu) (length arguments))
                            arguments) clu)]
                                                                                                                
         [else
          (interpret (foldl (lambda (k v environment) (env-update environment k v))
                            (closure-environment clu)
                            (take unknow-parms (length arguments))
                            arguments) clu)]))]
    ))


;-----------------------------------------------------------------------------------------
; Helpers: Builtins and closures
;-----------------------------------------------------------------------------------------

; Returns whether a given symbol refers to a procudure of Dubdub function
; (created with lambda) as well as a Dubdub builtin. 
(define (procedure? identifier)
  (cond
    [(symbol? identifier) (if (builtin? identifier) #t #f)]
    [(list? identifier) (or (equal? 'lambda (first identifier)) (builtin? (first identifier)))]
    [(number? identifier) #f]
    [(closure? identifier) #t]))

; A hash mapping symbols for Dubdub builtin functions to their corresponding Racket value.
(define builtins
  (hash
   '+ +
   'equal? equal?
   '< <
   'integer? integer?
   'boolean? boolean?
   ; Note: You'll almost certainly need to replace procedure? here to properly return #t
   ; when given your closure data structure at the end of Task 1!
   'procedure? procedure?
   ))

; Returns whether a given symbol refers to a builtin Dubdub function.
(define (builtin? identifier) (hash-has-key? builtins identifier))

#|
Starter definition for a closure "struct". Racket structs behave similarly to
C structs (contain fields but no methods or encapsulation).
Read more at https://docs.racket-lang.org/guide/define-struct.html.

You can and should modify this as necessary. If you're having trouble working with
Racket structs, feel free to switch this implementation to use a list/hash instead.
|#
(struct closure (contract environment params body))
                                                  
(define (env-update env key value) ;return a new env by adding key and value.
  (if (closure? value)
      (if (equal? (list) (closure-contract value))  ;binding a closure
          
          (if (hash-has-key? env key) ;closure with no contract 
              (hash-set env key (closure (closure-contract (hash-ref env key)) (closure-environment value) (closure-params value) (closure-body value)))
              (hash-set env key (closure (list) (closure-environment value) (closure-params value) (closure-body value))))
          
          (let ((num-unknown-parms (length (get-unknown-parms env (closure-params value)))))  ;closure has contract (currying)
            (env-update (contract-update env key (list-tail (closure-contract value) (- (length (closure-params value)) num-unknown-parms)))
                        key (closure (list) (closure-environment value) (closure-params value) (closure-body value))
            )))
      
      (if (hash-has-key? env key) ;binding a interger/boolean
          (report-error 'duplicate-name key)
          (hash-set env key value)) 
      ))

(define (contract-update env key contract)
  (if (hash-has-key? env key)
      
      (if (closure? (hash-ref env key));key exist in env
          
          (let ((value (hash-ref env key)))  ;the value of key is a closure.
            (if (equal? (list) (closure-contract value))
                
                (hash-set env key (closure contract (closure-environment value) (closure-params value) (closure-body value))) ;the closure do not have contract

                ((report-error 'invalid-contract key))))    ; the closure already have contract. Error raised.
         
          (report-error 'duplicate-name key))  ;key exist in env and not closure. Error raised.
      
      (hash-set env key (closure contract (list) (list) (list)))))  ;key not exist in env 


(define (closure-slovable env clu) ;return true iff all params in closure are defined 
  (foldl (lambda (parm result) (and result (hash-has-key? env parm))) #t (closure-params clu)))

(define (get-unknown-parms env parms) ;return a list of parms that do not have defined value in env
  (foldl (lambda (parm result) (if (hash-has-key? env parm) (append result (list)) (append result (list parm)))) (list) parms))

;return true if number of func_param equals number of predicate
;AND each of func_param satisfies corresponding predicate
;otherwise error raised
(define (precond_check env clo)
  (let ([predicates (take (closure-contract clo) (index-of (closure-contract clo) (quote ->)))]
        [params (foldl (lambda (param lst) (append lst (list (hash-ref env param)))) (list) (closure-params clo))])
    (if (equal? (length params) (length predicates))
        (if;checking if every argument satisfies the predicate in contract
         (foldl
          (lambda (pred param result) (if (equal? #f (equal? 'any pred)) (and result (interpret (hash) (append (list pred) (list param)))) (and result #t)))
          #t predicates params)
         #t
         (report-error 'contract-violation));if its contract is violated
        #f)));actual num of params and num of param defined in contract doesn't match


;return true if result of expr satisfies the post-condition in the contract
;otherwise, error raised
(define (postcond_check clo result)
  (let ([postcond (last (closure-contract clo))])
    (if (equal? #f (equal? 'any postcond))
        (if (interpret (hash) (append (list postcond) (list result))) #t (report-error 'contract-violation))
        #t)
    ))

;check if every predicate in contract is either a procedure or keyword "any"
;e.g. (integer? boolean? any -> procedure?))) returns true
;<con-expr> = <expr> | "any" ;
(define (check_contract con)
  (let* ([preconds (take con (index-of con (quote ->)))]
         [postcond (last con)]
         [pre_result (foldl
                      (lambda (pred result) (if (equal? #f (equal? 'any pred)) (and result (procedure? pred)) (and result #t))) #t preconds)]
         [post_result (or (procedure? postcond) (equal? 'any postcond))])
    (and pre_result post_result))
  )