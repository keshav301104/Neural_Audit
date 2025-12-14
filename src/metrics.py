import tiktoken

# Gemini 1.5 Flash Pricing (Approximate per 1k tokens)
INPUT_COST_PER_1K = 0.000075  # ~$0.075 per 1M input
OUTPUT_COST_PER_1K = 0.00030  # ~$0.30 per 1M output

def calculate_tech_metrics(query, context, response):
    try:
        # Simulate input payload
        full_input = query + context
        
        # Count tokens (Using cl100k_base as a proxy for Gemini tokenization)
        encoder = tiktoken.get_encoding("cl100k_base")
        input_tokens = len(encoder.encode(full_input))
        output_tokens = len(encoder.encode(response))
        
        # Calculate Cost
        cost = ((input_tokens / 1000) * INPUT_COST_PER_1K) + \
               ((output_tokens / 1000) * OUTPUT_COST_PER_1K)
        
        # Estimate Latency (Gemini Flash is fast, approx 80 tokens/sec)
        latency = round(output_tokens / 80.0, 2)
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost_usd": round(cost, 7),
            "latency_seconds": latency
        }
    except:
        return {"cost_usd": 0, "latency_seconds": 0}