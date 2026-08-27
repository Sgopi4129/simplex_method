# Simplex Studio

## Deploy with Docker

From the repository root:

```powershell
docker compose up --build
```

Open `http://localhost:3000`. The frontend container forwards calculations to the internal Python API container at `http://simplex-api:8000/solve`.

This setup works on Docker-capable hosting platforms. Deploy `frontend/Dockerfile` as the website on port 3000 and `backend/Dockerfile` as the API on port 8000. Set `SIMPLEX_BACKEND_URL` on the frontend service to the API URL ending in `/solve`.

## Deploy to Cloudflare Pages

The frontend also works as a static site because simplex calculations run in the browser. In Cloudflare Pages, use:

```text
Build command: corepack pnpm@11.17.0 build
Build output directory: out
Root directory: frontend
```

Do not use `npx wrangler deploy`; that command is for Workers. Cloudflare Pages deploys the generated `out` directory. The Python Docker API is only needed for the Docker deployment.
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

The frontend uses Next.js standalone output so its Docker image runs with `node server.js`.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

