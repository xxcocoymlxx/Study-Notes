#lang racket

(provide s-null s-null? s-cons s-first s-rest make-stream stream->list)

; Empty stream value, and check for empty stream.
(define s-null 's-null)

(define (s-null? stream) (equal? stream s-null))

#|
(s-cons <first> <rest>)
  <first>: A Racket expression.
  <rest>: A stream (e.g., s-null or another s-cons expression).

  Returns a new stream whose first value is <first>, and whose other
  items are the ones in <rest>. Unlike a regular list, both <first>
  and <rest> are wrapped in a thunk, so aren't evaluated until called.
|#
(define-syntax s-cons
  (syntax-rules ()
    [(s-cons <first> <rest>)
     (cons (thunk <first>) (thunk <rest>))]))

; These two define the stream-equivalents of "first" and "rest".
; We need to use `car` and `cdr` (similar to `first` and `rest`)
; for a technical reason that isn't important for this course.
; Note that s-rest both accesses the "rest thunk" and calls it,
; so that it does indeed return a stream.
(define (s-first stream) ((car stream)))

(define (s-rest stream) ((cdr stream)))

; Make a stream. We use macros so that the elements of the stream
; are not evaluated until they are used.
(define-syntax make-stream
  (syntax-rules ()
    [(make-stream) s-null]
    [(make-stream <first> <rest> ...)
     (s-cons <first> (make-stream <rest> ...))]))

; Convert a stream into a list
(define (stream->list s)
  (if (s-null? s)
      '()
      (cons (s-first s) (stream->list (s-rest s)))))
