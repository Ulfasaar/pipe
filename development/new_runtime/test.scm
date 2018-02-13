; (define run (step data) print step data)

; (define (pipe steps) 
;     ((lambda (data) (for-each run steps data))))   

; (define (a_step some_data)(print some_data))

; (pipe `(a_step))
; (for-each print `(1, 2, 3))

; ((pipe `(a_step)) 1)
