echo gauss2D
octave gaussClassifier.sh ../datos/gauss2DTr.gz ../datos/gauss2DTe.gz
echo gender
octave gaussClassifier.sh ../datos/genderTr.gz ../datos/genderTe.gz
echo iris
octave gaussClassifier.sh ../datos/irisTr.gz ../datos/irisTe.gz
echo news
octave gaussClassifier.sh ../datos/newsTr.gz ../datos/newsTe.gz
echo ocr20x20
octave gaussClassifier.sh ../datos/ocr20x20Tr.gz ../datos/ocr20x20Te.gz
echo videos
octave gaussClassifier.sh ../datos/videosTr.gz ../datos/videosTe.gz
