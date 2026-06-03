class TranscriptAgent:
    async def extract(self, page, adapter):
        return await adapter.extract_transcript(page)
