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
    [(equal? 1 (length prog)) (interpret (hash) (first prog))] ;no additional bindings and contracts, only <expr>
    ;normal prog (<binding_or_contract> ... <expr>)
    [else
     (interpret (foldl (lambda (expr env) (interpret env expr)) (hash) (take prog (- (length prog) 1))) (last prog))]
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
    ;the expr is closure structrue, recursion / return new closure
    [(closure? expr)
     (if (equal? #f (check-duplicates (closure-params expr)))
         (if (closure-slovable env expr)
             (if (equal? (list) (closure-contract expr)) (interpret env (closure-body expr));if no contract, return value
                 (if (precond_check env expr)
                     (let ([result (interpret env (closure-body expr))])
                       (if (postcond_check expr result) result (report-error 'contract-violation)))
                     (report-error 'invalid-contract (closure-funcname expr))))
             (closure (closure-contract expr) env (closure-params expr) (closure-body expr) (closure-funcname expr)))
         (report-error 'duplicate-name (check-duplicates (closure-params expr))))]  

    ;the expr is <expr> a number, return expr
    [(number? expr) expr]                                                                                                                                                      

    ;the expr is <expr> a boolean, return expr
    [(boolean? expr) expr]                                                                                                                                    

    ;the expr is <expr> a symbol, return Value / Error raised
    [(symbol? expr)
     (if (builtin? expr) (hash-ref builtins expr)
         (if (hash-has-key? env expr)
             (if (closure? (hash-ref env expr))
                 (if (equal? (list) (closure-body (hash-ref env expr)))
                     (report-error 'not-a-function (closure-funcname (hash-ref env expr)))
                     (hash-ref env expr))
                 (hash-ref env expr))
             (report-error 'unbound-name expr)))]


    ;the expr is <binding>, return new env / Error raised
    [(equal? (first expr) 'define)
     (env-update env (second expr) (interpret env (third expr)))]

    ;the expr is <contract>, return new env
    [(equal? (first expr) 'define-contract)
     (if (check_contract (third expr));if the predicates are procedure or "any"
         (contract-update env (second expr) (third expr))
         (report-error 'invalid-contract (second expr)))]

    ;the expr is <expr> function expresssion, return Clousre
    [(equal? (first expr) 'lambda)
     (if (equal? #f (check-duplicates (second expr)));if no duplicate parameters
         (closure (list) env (second expr) (third expr) (void))
         (report-error 'duplicate-name (check-duplicates (second expr))))]

    ;the epxr is a bulitin funciton call, recursion
    [(builtin? (first expr))
     (apply (hash-ref builtins (first expr))                                                                                                  
            (foldl (lambda (expr ls) (append ls (list (interpret env expr)))) (list) (rest expr)))] 

    
    ;the expr is NOT A FUNCTION CALL, error raised
    [(equal? #f (or (builtin? (first expr)) (closure? (interpret env (first expr)))))
     (report-error 'not-a-function (first expr))]                                                                                     


    ;the expr is <expr> a function call and followed by args of <expr>, recursion
    [else
     (let* ((clu (interpret env (first expr)))                                                                                              
            (arguments (foldl (lambda (exprsion results) (append results (list (interpret env exprsion)))) (list) (rest expr)))
            (unknow-parms (get-unknown-parms (closure-environment clu) (closure-params clu))))
       
       (cond
         
         ;if number of given arguments is larger than number of parameters, error raised
         [(> (length arguments) (length (closure-params clu)))
          (report-error 'arity-mismatch (length arguments) (length (closure-params clu)))]

         ;if number of given arguments is larger than number of paramters with unknown values
         [(> (length arguments) (length unknow-parms))
          (if (equal? #f (check-duplicates (closure-params clu)))
              (interpret (foldl (lambda (k v environment) (hash-set environment k v))
                                (closure-environment clu)
                                (take (closure-params clu) (length arguments))
                                arguments) clu)
              (report-error 'duplicate-name (check-duplicates (closure-params clu))))]

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

a closure struct that stores contract, environment, params, function body
of a function and function_name.
|#
(struct closure (contract environment params body funcname))


;-----------------------------------------------------------------------------------------
; Helpers: Environment and Contract update
;-----------------------------------------------------------------------------------------
#|
(env-update env key value) -> hash

  key: a function name
  value: could be a single integer/boolean/closure
  env: a hash table that stores bindings

  Update current env with given key and value
  if there are duplicate names, error raised.
|#
(define (env-update env key value)
  ;binding a closure
  (if (closure? value)
      
      (if (equal? (list) (closure-contract value))
          
          ;if the given [value] does not have contract
          (if (hash-has-key? env key)
              ;if the given [value] does not have contract but the key already exists, add the new function to closure
              (hash-set env key (closure (closure-contract (hash-ref env key)) (closure-environment value) (closure-params value) (closure-body value) key))
              ;if the closure does not have contract and the key does not exists, add the new function
              (hash-set env key (closure (list) (closure-environment value) (closure-params value) (closure-body value) key)))

          ;closure already has contract (currying)
          ;use contract-update to update the contract after currying
          (let ((num-unknown-parms (length (get-unknown-parms env (closure-params value)))))
            (env-update (contract-update env key (list-tail (closure-contract value) (- (length (closure-params value)) num-unknown-parms)))
                        key
                        (closure (list) (closure-environment value) (list-tail (closure-params value) (- (length (closure-params value)) num-unknown-parms)) (closure-body value) key)
                        )))

      ;binding a interger/boolean
      (if (hash-has-key? env key) (report-error 'duplicate-name key) (hash-set env key value)) 
      ))



#|
(contract-update env key contract) -> hash

  key: a function name
  contract: contract of a given function [key]
  env: a hash table that stores bindings

  Update current env with given key and contract
  also error checking if duplicate contract exists,
  if so, error raised.
|#
(define (contract-update env key contract)
  (if (hash-has-key? env key);key exists in env
      
      (if (closure? (hash-ref env key));the value of key is a closure
          
          (let ((value (hash-ref env key)))
            
            (if (equal? (list) (closure-contract value));if there are no existing contract
                
                (hash-set env key (closure contract (closure-environment value) (closure-params value) (closure-body value) key)) ;add the contract to the closure

                ((report-error 'invalid-contract key)))); the closure already have contract, error raised.
         
          (report-error 'duplicate-name key))  ;key exist in env and not closure, error raised.
      
      (hash-set env key (closure contract (list) (list) (list) key))))  ;key not exist in env, add contract to an empty closure



;-----------------------------------------------------------------------------------------
; Helpers: status check of function parameters
;-----------------------------------------------------------------------------------------
#|
(closure-slovable env closure) -> boolean
  correct function name shoule be: closure-solvable

  clo: a closure of a function
  env: current env when a function is ready to be evaluated

  Return true if and only if all paramaters in closure have a
  defined value in env.
|#
(define (closure-slovable env clu)
  (foldl (lambda (parm result) (and result (hash-has-key? env parm))) #t (closure-params clu)))



#|
(get-unknown-parms env params) -> list
  params: list of parameters of a function
  env: current env when the parameter of a function is checked

  Return a list of parameters that do not have defined value in env
|#
(define (get-unknown-parms env parms)
  (foldl (lambda (parm result) (if (hash-has-key? env parm) (append result (list)) (append result (list parm)))) (list) parms))



;-----------------------------------------------------------------------------------------
; Helpers: Contracts
;-----------------------------------------------------------------------------------------

#|
(precond_check env closure) -> boolean
  clo: a closure of a function with contracts
  env: current env when a function is ready to be evaluated

  return true if number of params equals number of predicates
  in the contracts, AND each of parameters satisfies corresponding
  predicate. Otherwise, error raised.
|#
(define (precond_check env clo)
  (let ([predicates (take (closure-contract clo) (index-of (closure-contract clo) (quote ->)))]
        ;get the value of each paramater from env
        [params (foldl (lambda (param lst) (append lst (list (hash-ref env param)))) (list) (closure-params clo))])
    (if (equal? (length params) (length predicates))
        (if;checking if every argument satisfies the predicate in contract
         (foldl
          (lambda (pred param result) (if (equal? #f (equal? 'any pred)) (and result (interpret (hash) (append (list pred) (list param)))) (and result #t)))
          #t predicates params)
         #t
         (report-error 'contract-violation));if its contract is violated
        #f)));actual num of params and num of param defined in contract doesn't match



#|
(postcond_check closure result) -> boolean
  clo: a closure of a function with contracts
  result: return value of a function, it could be a single number,
          boolean, closure, etc.

  Return true if result of expr satisfies the post-condition in the contract,
  otherwise, error raised
|#
(define (postcond_check clo result)
  (let ([postcond (last (closure-contract clo))])
    (if (equal? #f (equal? 'any postcond))
        (if (interpret (hash) (append (list postcond) (list result))) #t (report-error 'contract-violation))
        #t)
    ))


#|
(check_contract con) -> boolean
  con: datum?
    A syntactically-valid Dubdub expression of contracts with following format:
     <contract> = "(" "define-contract" ID "(" <con-expr> ... "->" <con-expr> ")" ")" ;
    ;<con-expr> = <expr> | "any" ;
     e.g. (integer? boolean? any -> procedure?))) returns true

  Check if every predicate in contract is either a procedure or keyword "any".
|#
(define (check_contract con)
  (let* ([preconds (take con (index-of con (quote ->)))]
         [postcond (last con)]
         [pre_result (foldl
                      (lambda (pred result) (if (equal? #f (equal? 'any pred)) (and result (procedure? pred)) (and result #t))) #t preconds)]
         [post_result (or (procedure? postcond) (equal? 'any postcond))])
    (and pre_result post_result))
  )