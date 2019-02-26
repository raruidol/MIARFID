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
	c6 - contenedor
	c7 - contenedor
	c8 - contenedor
	c9 - contenedor
	c10 - contenedor
	c11 - contenedor
	p1 - pallet
	p2 - pallet
	p3 - pallet
	p4 - pallet
	p5 - pallet
	p6 - pallet

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
	(esta_en p3 muelle1)
	(esta_en p4 muelle2)
	(esta_en p5 muelle2)
	(esta_en p6 muelle2)

	(esta_en c7 muelle1)
	(esta_en c1 muelle1)
	(esta_en c9 muelle1)
	(esta_en c10 muelle1)
	(esta_en c11 muelle1)
	(encima c7 c1)
	(encima c1 p1)
	(tope c7 p1)
	(= (altura p1) 2)
	(disponible c7)
	(disponible c1)
	(encima c10 c9)
	(encima c9 p2)
	(tope c10 p2)
	(= (altura p2) 2)
	(disponible c10)
	(encima c11 p3)
	(tope c11 p3)
	(= (altura p3) 1)
	(disponible c11)

	(esta_en c2 muelle2)
	(esta_en c3 muelle2)
	(esta_en c4 muelle2)
	(esta_en c5 muelle2)
	(esta_en c6 muelle2)
	(esta_en c8 muelle2)
	(encima c8 c4)
	(encima c4 p4)
	(tope c8 p4)
	(= (altura p4) 2)
	(disponible c8)
	(encima c2 c3)
	(encima c3 c5)
	(encima c5 p5)
	(tope c2 p5)
	(= (altura p5) 3)
	(disponible c2)
	(encima c6 p6)
	(tope c6 p6)
	(= (altura p6) 1)
	(disponible c6)

	(es_objetivo c7)
	(es_objetivo c4)
	(es_objetivo c3)
	(es_normal c1)
	(es_normal c2)
	(es_normal c5)
	(es_normal c6)
	(es_normal c8)
	(es_normal c9)
	(es_normal c10)
	(es_normal c11)


	(=(peso c1) 5)
	(=(peso c2) 5)
	(=(peso c3) 10)
	(=(peso c4) 5)
	(=(peso c5) 4)
	(=(peso c6) 3)
	(=(peso c7) 9)
	(=(peso c8) 4)
	(=(peso c9) 5)
	(=(peso c10) 3)
	(=(peso c11) 3)


	(=(tiempo-mover cinta1) 5)
	(=(tiempo-mover cinta2) 5)


	(= (max_alt muelle1) 3)
	(= (max_alt muelle2) 3)



)

(:goal (and
        (disponible c7)
				(disponible c4)
				(disponible c3)
				(esta_en c7 muelle1)
				(esta_en c4 muelle1)
				(esta_en c3 muelle1)
    )
)

(:metric minimize (total-time))
)
