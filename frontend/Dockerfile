# imagen Node.js
FROM node:22-alpine

# directorio de trabajo
WORKDIR /app

# instalacion de dependencias
COPY package.json package-lock.json* ./
RUN npm install

# copia el contenido del proyecto al contenedor
COPY . .

# expone el puerto por defecto de Vite
EXPOSE 5173

# comando para iniciar React. "--host" (permite conexiones externas)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]