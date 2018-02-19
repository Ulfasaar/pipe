; (define run (step data) print step data)

; (define (pipe steps) 
;     (
;         (let ([prev_result 0]) prev_result)

;         (define (run step, data) (set! prev_result (data step)))
            
;         (lambda (data)
;             (for-each run steps data) prev_result)))
           

; (define (a_step some_data)(print some_data))

; (pipe `(a_step))
; (for-each print `(1, 2, 3))

; ((pipe `(a_step)) 1)

(define hi (print "hi"))

; (print "hi")
; (apply print `("hi"))
