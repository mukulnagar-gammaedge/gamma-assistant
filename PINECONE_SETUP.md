# Pinecone Setup Guide for AI Assistant

## Prerequisites
- Pinecone account (free tier available at https://www.pinecone.io/)
- API Key from Pinecone

## Step 1: Create Pinecone Index

1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Create a new index with these settings:
   - **Name**: `ai-assistant` (or change `PINECONE_INDEX_NAME` in render.yaml)
   - **Dimension**: `384` (matches all-MiniLM-L6-v2 embedding model)
   - **Metric**: `cosine` (for similarity search)
   - **Region**: Choose closest to your location

3. Wait for index to initialize (~1 minute)

## Step 2: Get Your API Key

1. In Pinecone Console, go to "API Keys"
2. Copy your API Key (you may need to create one)

## Step 3: Set Environment Variables

### Local Development (.env file)
```
PINECONE_API_KEY=your-api-key-here
PINECONE_INDEX_NAME=ai-assistant
GROQ_API_KEY=your-groq-key
```

### Render Deployment
The environment variables are already configured in `render.yaml`:
- `PINECONE_API_KEY` - Set this in Render dashboard (secret)
- `PINECONE_INDEX_NAME` - Already set as `ai-assistant`

## Step 4: Deploy

1. **Local Testing**:
   ```bash
   python -m pip install -r requirements.txt
   python -m uvicorn app.main:app --reload
   ```

2. **Render Deployment**:
   - Push changes to git: `git push`
   - In Render dashboard, set `PINECONE_API_KEY` secret
   - Deploy will auto-trigger

## Important Changes Made

### Files Updated:
- ✅ `render.yaml` - Added Pinecone env vars
- ✅ `requirements.txt` - Added `pinecone-client==5.2.0`
- ✅ `app/ingestion.py` - Now uses Pinecone instead of local FAISS
- ✅ `app/retrieval.py` - Now queries Pinecone instead of local FAISS

### New File:
- ✅ `app/pinecone_utils.py` - Pinecone integration module

## How It Works

### Document Ingestion Flow:
1. Upload PDF → Extract text → Chunk (50 words each)
2. Generate embeddings (384-dimensional using all-MiniLM-L6-v2)
3. **Upsert to Pinecone** (replaces local FAISS storage)

### Query Flow:
1. User asks question
2. Encode query to 384-dimensional embedding
3. **Search Pinecone** (similarity search using cosine metric)
4. Return top-5 results with similarity scores
5. Re-rank using CrossEncoder for final top-3 results
6. Send context to Groq API for response

## Key Differences from FAISS

| Aspect | FAISS | Pinecone |
|--------|-------|----------|
| **Storage** | Local disk | Cloud |
| **Metric** | L2 Distance | Cosine Similarity |
| **Scalability** | Limited by disk | Elastic |
| **Persistence** | Manual save/load | Automatic |
| **Free Tier** | Unlimited local use | 125K vectors/month |

## Troubleshooting

### Error: "PINECONE_API_KEY not set"
- Make sure environment variable is configured (local: .env, Render: dashboard)

### Error: "Could not access Pinecone index"
- Verify index exists in Pinecone console
- Check index dimension is 384
- Confirm API key is correct

### Low similarity scores
- Default threshold is 0.2 (on 0-1 scale where 1 is perfect match)
- Can adjust threshold in `app/retrieval.py` search() function
- Improve with better chunking strategy

### Pinecone Free Tier Limits
- 125K vectors/month (approximately 25K PDF documents)
- 1 free index
- Contact Pinecone for higher limits

## Next Steps

1. Test locally with `.env` file
2. Deploy to Render and set PINECONE_API_KEY
3. Upload documents via `/upload` endpoint
4. Test queries via chat interface

Happy querying! 🚀
