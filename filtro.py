import cv2
import imutils

# Vídeo de entrada
cap = cv2.VideoCapture(0)

# Leitura da imagem para colocar no vídeo
image = cv2.imread('gorro_navidad.PNG', cv2.IMREAD_UNCHANGED)
#image = cv2.imread('tiara.png', cv2.IMREAD_UNCHANGED)
#image = cv2.imread('2021.png', cv2.IMREAD_UNCHANGED)
#image = cv2.imread('monophy.gif', cv2.IMREAD_UNCHANGED)

# Detector de rostos
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#img = 0

while True:

	#img = 0

	ret, frame = cap.read()
	if ret == False: break
	frame = imutils.resize(frame, width=640)

	# Detecção dos rostos presentes na webcan
	faces = faceClassif.detectMultiScale(frame, 1.3, 5)

	for (x, y, w, h) in faces:
		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
 
		# Redimensionar a imagem do filtro de acordo com a largura do rosto detectado
		
		resized_image = imutils.resize(image, width=w)
		filas_image = resized_image.shape[0]
		col_image = w

		# Determinar uma parte da altura da imagem de entrada 
		# redimensionada
		porcion_alto = filas_image // 4

		dif = 0

		# Se houver espaço suficiente acima do rosto detectado
		# para inserir a imagem de entrada redimensionada
		# essa imagem será exibida
		if y + porcion_alto - filas_image >= 0:

			# Pegamos a seção do frame, onde estará localizado
			# o gorro/tiara
			n_frame = frame[y + porcion_alto - filas_image : y + porcion_alto,
				x : x + col_image]
		else:
			# Determinamos a seção da imagem que excede a do vídeo
			dif = abs(y + porcion_alto - filas_image) 
			# Pegamos a seção do frame, onde ela estará localizado
			# o gorro/tiara
			n_frame = frame[0 : y + porcion_alto,
				x : x + col_image]

		# Determinamos a máscara que a imagem de entrada tem
		# redimensionada e também a invertemos
		mask = resized_image[:, :, 3]
		mask_inv = cv2.bitwise_not(mask)
			
		# Criamos uma imagem com fundo preto e o gorro/tiara/2021
		# Em seguida, criamos uma imagem onde no fundo está o frame
		# e de preto o gorro/tiara/2021
		bg_black = cv2.bitwise_and(resized_image, resized_image, mask=mask)
		bg_black = bg_black[dif:, :, 0:3]
		bg_frame = cv2.bitwise_and(n_frame, n_frame, mask=mask_inv[dif:,:])

		# Adicionamos as duas imagens obtidas
		result = cv2.add(bg_black, bg_frame)
		if y + porcion_alto - filas_image >= 0:
			frame[y + porcion_alto - filas_image : y + porcion_alto, x : x + col_image] = result

		else:
			frame[0 : y + porcion_alto, x : x + col_image] = result
		
	cv2.imshow('frame',frame)

	key = cv2.waitKey(1)
	if key == 32:
	# 	#img = 1
		cv2.imwrite("FotoFiltro.png", frame)
	elif key == 27:
		break

cap.release()
cv2.destroyAllWindows()