#lang racket #| CSC324 Fall 2019: Exercise 6 |#
#|
* Before starting, please review the exercise guidelines at
http://www.cs.toronto.edu/~lczhang/324/homework.html *
|#
;-------------------------------------------------------------------------------
(provide my-class-getter)

; Return a function that raises an attribute error (with an appropriate message).
(define (attribute-error object attr)
  (lambda () (error (format "~a has no attribute ~a." object attr))))

;-------------------------------------------------------------------------------
; * Task 1: Accessor functions in `my-class` *
;-------------------------------------------------------------------------------
#|
(my-class-getter <Class> (<attr> ...)
  (method (<method-name> <param> ...) <body>) ...)

  This macro accepts the *exact* same pattern as my-class from lecture,
  and defines a constructor function that behaves in the same way as well.

  In addition to defining the constructor, my-class-getter defines
  *one new accessor function per attribute of the class*, using the name
  of the attribute as the name of the function.

  Implementation notes:
    - Our starter code has wrapped the `define` from lecture inside a `begin`.
      This is required so that you can add more `define`s after the one for the
      constructor.
|#
(define-syntax my-class-getter
  (syntax-rules (method)
    [(my-class <Class>
               (<attr> ...)
               (method (<method-name> <params> ...) <body>) ...)
     (begin
       ; Construct a class-level hash table consisting of all the methods
       (define class__dict__
         (make-immutable-hash (list
                               (cons (quote <method-name>)
                                     (lambda (<params> ...) <body>))
                               ...)))
       
       ; It is possible to do this assignment by only adding new
       ; expression(s) here!
       (define (<attr> <class-id>)
         (<class-id> (quote <attr>)))
       ...
       
       ; Build the constructor
       (define (<Class> <attr> ...)
         (letrec
             ; Construct an object-level hash table consisting of the attributes
             ([self__dict__
               (make-immutable-hash
                (list (cons (quote <attr>) <attr>) ...))]
              [me (lambda (attr)
                    (cond
                      [(hash-has-key? self__dict__ attr)
                       (hash-ref self__dict__ attr)]
                      [(hash-has-key? class__dict__ attr)
                       (fix-first me (hash-ref class__dict__ attr))]
                      [else
                       ((attribute-error (quote <Class>) attr))]))])
           me)))]))

; The helper-function `fix-first`
(define (fix-first x f)
  (lambda rest (apply f (cons x rest))))


(module+ test
  (require rackunit)

  ; We use `local` to create a local scope for our definitions.
  ; Run these tests when you're ready!
  (local
      [(my-class-getter Point (x y)
                        (method (size self)
                                (sqrt (+ (* (self 'x) (self 'x))
                                         (* (self 'y) (self 'y)))))
                        (method (scale self n)
                                (Point (* (self 'x) (self 'n))
                                       (* (self 'y) (self 'n)))))]
      (test-true "x and y are functions" (and (procedure? x) (procedure? y)))
      (test-equal? "x and y are accessors"
                   (let ([p (Point 2 3)])
                     (list (x p) (y p)))
                   (list 2 3))))
