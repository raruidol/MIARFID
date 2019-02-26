(define (domain puerto)

(:requirements :typing :equality)

(:types muelle numero cinta base grua - object
	    contenedor pallet - base)



  (:predicates
    (esta_en ?x - (either grua contenedor pallet) ?m - muelle)
    (encima ?c - contenedor ?a - base )
    (sucesor ?n1 - numero ?n0 - numero ?m - muelle)
    (sujetando ?g - grua ?c - contenedor)
    (libre ?a - (either grua cinta))
    (colocado_en ?c - contenedor ?ci - cinta)
    (cinta_de_a ?ci - cinta ?m1 - muelle ?m2 - muelle)
	(es_objetivo ?c - contenedor)
	(es_normal ?c - contenedor)
	(disponible ?c - base)
	(tope ?t - base ?p - pallet)
	(max_alt ?n - numero ?m - muelle)
	(altura ?n - numero ?p - pallet)
  )

	(:action stack-container
		:parameters (?g - grua ?c1 - contenedor ?c2 - base ?p - pallet ?m - muelle ?n - numero ?n1 - numero)
		:precondition ( and (sujetando ?g ?c1) (tope ?c2 ?p) (esta_en ?p ?m) (esta_en ?g ?m) (es_normal ?c1) (altura ?n ?p) (sucesor ?n ?n1 ?m))
		:effect ( and (tope ?c1 ?p) (not (tope ?c2 ?p)) (not (disponible ?c2)) (disponible ?c1) (esta_en ?c1 ?m) (not (sujetando ?g ?c1)) (libre ?g) (altura ?n1 ?p) (not (altura ?n ?p)) (encima ?c1 ?c2) )
	)

	(:action objectivestack-container
		:parameters (?g - grua ?c1 - contenedor ?c2 - base ?p - pallet ?m - muelle ?n - numero ?n1 - numero)
		:precondition ( and (sujetando ?g ?c1) (tope ?c2 ?p) (esta_en ?p ?m) (esta_en ?g ?m) (es_objetivo ?c1) (altura ?n ?p) (sucesor ?n ?n1 ?m))
		:effect ( and (tope ?c1 ?p) (not (tope ?c2 ?p)) (disponible ?c1) (esta_en ?c1 ?m) (not (sujetando ?g ?c1)) (libre ?g) (altura ?n1 ?p) (not (altura ?n ?p)) (encima ?c1 ?c2) )
	)

	(:action unstack-container
		:parameters (?g - grua ?c1 - contenedor ?b - base ?p - pallet ?m - muelle ?n1 - numero ?n2 - numero)
		:precondition ( and (libre ?g) (tope ?c1 ?p) (esta_en ?p ?m) (esta_en ?c1 ?m) (esta_en ?g ?m)(sucesor ?n1 ?n2 ?m) (altura ?n2 ?p) (encima ?c1 ?b))
		:effect ( and (not (libre ?g)) (not (tope ?c1 ?p)) (tope ?b ?p) (not (esta_en ?c1 ?m)) (altura ?n1 ?p) (not (altura ?n2 ?p)) (not (encima ?c1 ?b)) (sujetando ?g ?c1) (not (disponible ?c1)) (disponible ?b) )
	)

	(:action dejar-en-cinta
		:parameters (?g - grua ?c - contenedor ?m1 - muelle ?m2 - muelle ?ci - cinta)
		:precondition ( and (sujetando ?g ?c) (libre ?ci) (esta_en ?g ?m1) (cinta_de_a ?ci ?m1 ?m2) )
		:effect ( and ( not(sujetando ?g ?c)) (not (libre ?ci)) (colocado_en ?c ?ci) (libre ?g))
	)

	(:action coger-de-cinta
   :parameters (?g - grua ?c - contenedor ?m1 - muelle ?m2 - muelle ?ci - cinta)
   :precondition ( and (colocado_en ?c ?ci) (cinta_de_a ?ci ?m1 ?m2) (esta_en ?g ?m2) (libre ?g) )
   :effect ( and (sujetando ?g ?c) (libre ?ci) (not (libre ?g)) (not (colocado_en ?c ?ci)))
	)
)
