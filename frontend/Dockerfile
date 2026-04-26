FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

RUN npm run build

CMD ["sh", "-c", "npm run start -- --port ${PORT:-5173}"]
