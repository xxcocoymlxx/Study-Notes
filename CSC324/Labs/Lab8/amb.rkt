#lang racket

(require racket/control)
(require "streams.rkt")

(provide do/-< -< -<< next! fail)

#|
(next! <g>)
  <g>: A stream

  Returns the first element of the stream. Then, mutate the stream
  value to the rest of the stream. (This is version 2 of next! from
  the posted notes)
|#
(define-syntax next!
  (syntax-rules ()
    [(next! <g>)  ; in this version of next!, <g> is a thunk that evaluates to a stream
     (let* ([stream (<g>)]) ; first, evaluate <g>, that's why we have a bracket around it
       (if (s-null? stream)
           'DONE
           (begin
               (set! <g> (cdr stream)) ; use cdr rather than s-rest (why??)
               (s-first stream))))]))


; Every expression that uses `-<` should be wrapped with a `do/-<` as a
; delimiter(定界符)
(define-syntax do/-<
  (syntax-rules ()
     [(do/-< <expr>) (thunk (reset (singleton <expr>)))]))

; Helper function to create a stream with a single element
(define (singleton x) (make-stream x))

; The ambiguous choice operator
(define (-< . lst)
  (shift k (s-append-map k lst)))

(define-syntax -<<
  (syntax-rules ()
    [(-<< <c> ...)
     (shift k (s-append-map k (list <c> ...)))]))

;(define-syntax -<<
; (syntax-rules ()
;   [(-<< <c>) (shift k (k <c>))]
;   [(-<< <c> <d> ...)
;    (shift k (s-append (k <c>) (k (-<< <d> ...))))]))
;     (shift k (s-append-map k (list <c> ...)))]))


; Append together the stream s, and a thunk t that produces a second stream
(define (s-append s t)
  (cond 
    [(s-null? s) (t)]
    [(pair? s) (s-cons (s-first s) (s-append (s-rest s) t))]
    [else
     (s-cons s (t))]))

; Apply k to every item of lst, then append together the resulting streams
(define (s-append-map k lst)
  (if (empty? lst)
      s-null
      (s-append (k (first lst));evaluate the first item
                (thunk (s-append-map k (rest lst))))));but don't evaluate the rest YET

;backtracking
(define (fail) (shift k s-null))


