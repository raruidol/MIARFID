(define (domain puerto)

(:requirements :typing :equality :durative-actions :fluents)

(:types muelle cinta base grua - object
	    contenedor pallet - base)

  (:predicates
    (esta_en ?x - (either grua contenedor pallet) ?m - muelle)
    (encima ?c - contenedor ?a - base )
    (sujetando ?g - grua ?c - contenedor)
    (libre ?a - (either grua cinta))
    (colocado_en ?c - contenedor ?ci - cinta)
    (cinta_de_a ?ci - cinta ?m1 - muelle ?m2 - muelle)
	(es_objetivo ?c - contenedor)
	(es_normal ?c - contenedor)
	(disponible ?c - base)
	(tope ?t - base ?p - pallet)
	(max_alt ?m - muelle)
	(altura ?p - pallet)
	(movido ?c - contenedor ?ci - cinta)
  )
  
  (:functions
     (max_alt ?m - muelle) 
     (altura ?p - pallet)
     (peso ?c - contenedor)
     (tiempo-mover ?ci - cinta)
  )

	(:durative-action stack-container
		:parameters (?g - grua ?c1 - contenedor ?c2 - base ?p - pallet ?m - muelle)
		:duration (= ?duration (+(- 5 (+ 1 (altura ?p))) (/ (peso ?c1) 10)   )    )
		:condition (and (over all(sujetando ?g ?c1)) (over all(tope ?c2 ?p)) (over all(esta_en ?p ?m)) (over all(esta_en ?g ?m)) (over all(es_normal ?c1)) (over all(<(altura ?p) (max_alt ?m))) )
		:effect (and (at end(tope ?c1 ?p)) (at end(not (tope ?c2 ?p))) (at end(not (disponible ?c2))) (at end(disponible ?c1)) (at end(esta_en ?c1 ?m)) (at end(not (sujetando ?g ?c1)))
		 (at end(libre ?g)) (at end(increase (altura ?p) 1 )) (at end(encima ?c1 ?c2)))
	)

	(:durative-action objectivestack-container
		:parameters (?g - grua ?c1 - contenedor ?c2 - base ?p - pallet ?m - muelle)
		:duration (= ?duration (+(- 5 (+ 1 (altura ?p))) (/  (peso ?c1) 10)   )    )
		:condition (and (over all(sujetando ?g ?c1)) (over all(tope ?c2 ?p)) (over all(esta_en ?p ?m)) (over all(esta_en ?g ?m)) (over all(es_objetivo ?c1))  (over all(<(altura ?p) (max_alt ?m))) )
		:effect (and (at end(tope ?c1 ?p)) (at end(not (tope ?c2 ?p))) (at end(disponible ?c1)) (at end(esta_en ?c1 ?m)) (at end(not (sujetando ?g ?c1))) (at end(libre ?g)) 
			(at end(increase (altura ?p) 1 )) (at end(encima ?c1 ?c2) )  )
	)

	(:durative-action unstack-container
		:parameters (?g - grua ?c1 - contenedor ?b - base ?p - pallet ?m - muelle)
		:duration (= ?duration (+(- 5 (altura ?p)) (/  (peso ?c1) 10))    )
		:condition (and (at start(libre ?g)) (over all(tope ?c1 ?p)) (over all(esta_en ?p ?m)) (over all(esta_en ?c1 ?m)) (over all(esta_en ?g ?m)) (over all(encima ?c1 ?b)) ) 
		:effect (and (at start(not (libre ?g))) (at end(not (tope ?c1 ?p))) (at end(tope ?b ?p)) (at end(not (esta_en ?c1 ?m))) (at end(decrease (altura ?p) 1)) (at end(not (encima ?c1 ?b))) (at end(sujetando ?g ?c1)) (at start(not (disponible ?c1))) (at end(disponible ?b)) )
	)

	(:durative-action dejar-en-cinta
		:parameters (?g - grua ?c - contenedor ?m1 - muelle ?m2 - muelle ?ci - cinta)
		:duration (= ?duration (+ 2 (/  (peso ?c) 10))    )
		:condition (and (over all(sujetando ?g ?c)) (over all(libre ?ci)) (over all(esta_en ?g ?m1)) (over all(cinta_de_a ?ci ?m1 ?m2)) )
		:effect (and (at end( not(sujetando ?g ?c))) (at start(not (libre ?ci))) (at end(colocado_en ?c ?ci)) (at end(libre ?g)))
	)


	(:durative-action mover-cinta
	   :parameters (?c - contenedor ?m1 - muelle ?m2 - muelle ?ci - cinta)
	   :duration (= ?duration (tiempo-mover ?ci) )
	   :condition (and (over all(colocado_en ?c ?ci)) (over all(cinta_de_a ?ci ?m1 ?m2))  )
	   :effect (and (at end(movido ?c ?ci)) )
	)

	(:durative-action coger-de-cinta
	   :parameters (?g - grua ?c - contenedor ?m1 - muelle ?m2 - muelle ?ci - cinta)
	   :duration (= ?duration (+ 2 (/  (peso ?c) 10))    )
	   :condition (and (over all(colocado_en ?c ?ci)) (over all(cinta_de_a ?ci ?m1 ?m2)) (over all(esta_en ?g ?m2)) (over all(libre ?g)) (over all(movido ?c ?ci)) )
	   :effect (and (at end(sujetando ?g ?c)) (at end(libre ?ci)) (at start(not (libre ?g))) (at start(not (colocado_en ?c ?ci))) (at end(not (movido ?c ?ci)))
	))



)
