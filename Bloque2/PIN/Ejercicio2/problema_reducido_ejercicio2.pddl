(define(problem puerto1)
(:domain puerto)

(:objects
	grua1 - grua
	grua2 - grua
	muelle1 - muelle
	muelle2 - muelle
	cinta1 - cinta
	cinta2 - cinta
	c1 - contenedor
	c2 - contenedor
	c3 - contenedor
	c4 - contenedor
	c5 - contenedor
	p1 - pallet
	p2 - pallet
	p3 - pallet
	p4 - pallet

)

(:init
	(esta_en grua1 muelle1)
	(libre grua1)
	(esta_en grua2 muelle2)
	(libre grua2)

	(cinta_de_a cinta1 muelle1 muelle2)
	(libre cinta1)
	(cinta_de_a cinta2 muelle2 muelle1)
	(libre cinta2)

	(esta_en p1 muelle1)
	(esta_en p2 muelle1)
	(esta_en p3 muelle2)
	(esta_en p4 muelle2)

	(esta_en c4 muelle1)
	(esta_en c5 muelle1)
	(encima c5 c4)
	(encima c4 p1)
	(tope c5 p1)
	(= (altura p1) 2)
	(disponible c5)
	
	(= (altura p2) 0)


        (esta_en c1 muelle2)
	(esta_en c2 muelle2)
	(esta_en c3 muelle2)
	
	(encima c1 p3)
	(tope c1 p3)
	(= (altura p3) 1)
	(disponible c1)
	
	(encima c2 c3)
	(encima c3 p4)
	(tope c2 p4)
	(= (altura p4) 2)
	(disponible c2)
	

	(es_objetivo c4)
	(es_objetivo c1)
	(es_objetivo c3)
	(es_normal c2)
	(es_normal c5)
	
	(=(peso c1) 5)
	(=(peso c2) 5)
	(=(peso c3) 5)
	(=(peso c4) 5)
	(=(peso c5) 5)


	(= (max_alt muelle1) 3)
	(= (max_alt muelle2) 3)



)

(:goal (and
        (disponible c1)
				(disponible c3)
				(disponible c4)
				(esta_en c1 muelle1)
				(esta_en c3 muelle1)
				(esta_en c4 muelle1)
    )
)

(:metric minimize (total-time))
)
