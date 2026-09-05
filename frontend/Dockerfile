FROM node:22-alpine AS build

WORKDIR /app

ARG API_BASE_URL
ENV VITE_API_BASE_URL=$API_BASE_URL
ARG DOCUMENTS_MAX_UPLOAD_BYTES
ENV VITE_DOCUMENTS_MAX_UPLOAD_BYTES=$DOCUMENTS_MAX_UPLOAD_BYTES
ARG DOCUMENTS_FORMATS
ENV VITE_DOCUMENTS_FORMATS=$DOCUMENTS_FORMATS

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.29-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
