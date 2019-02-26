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
	n0 - numero
	n1 - numero
	n2 - numero
	n3 - numero
	n4 - numero
	n5 - numero
	n6 - numero
	n7 - numero
	n8 - numero
	n9 - numero
	n10 - numero
	n11 - numero
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
	(altura n2 p1)
	(disponible c7)
	(disponible c1)
	(encima c10 c9)
	(encima c9 p2)
	(tope c10 p2)
	(altura n2 p2)
	(disponible c10)
	(encima c11 p3)
	(tope c11 p3)
	(altura n1 p3)
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
	(altura n2 p4)
	(disponible c8)
	(encima c2 c3)
	(encima c3 c5)
	(encima c5 p5)
	(tope c2 p5)
	(altura n3 p5)
	(disponible c2)
	(encima c6 p6)
	(tope c6 p6)
	(altura n1 p6)
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

	(sucesor n0 n1 muelle1)
	(sucesor n1 n2 muelle1)

	(sucesor n0 n1 muelle2)
	(sucesor n1 n2 muelle2)
	(sucesor n2 n3 muelle2)




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
