
Deploy checklist and commands (concise):

1) Prepare repo (locally):
   git clone <your-repo-url>
   unzip atendente-enem.zip (or copy files into repo)
   cd repo-root
   git add .
   git commit -m "Add Atendente ENEM starter"
   git push origin main

2) Render - backend:
   - Create new Web Service -> Connect to GitHub repo
   - Build command: pip install -r backend/requirements.txt
   - Start command: uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   - Set Environment Variables: DATABASE_URL, ZAPI_INSTANCE_ID, ZAPI_TOKEN, OPENAI_API_KEY (optional), SECRET_KEY, FRONTEND_URL
   - Deploy

3) Vercel - frontend:
   - Import project and select frontend directory
   - Set Environment Variable: NEXT_PUBLIC_API_URL to backend URL
   - Deploy

4) Z-API webhook:
   - In Z-API dashboard set Webhook URL to: https://<your-backend>/api/webhooks/whatsapp

5) Test via curl:
   curl https://<your-backend>/api/health
   curl -X POST "https://<your-backend>/api/webhooks/whatsapp" -H "Content-Type: application/json" -d '{"message":{"text":"oi","from":"5511999999999"}}'
