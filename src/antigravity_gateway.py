"""
Antigravity API Gateway - Unified API Management for All Agents and MCPs.

This module provides a centralized API gateway that routes all agent and MCP
requests through a single Antigravity API key, eliminating the need for
multiple API keys and providing unified billing, rate limiting, and monitoring.

Features:
- Single API key for all services (Gemini, Claude, OpenAI, etc.)
- Automatic model routing based on task complexity
- Built-in rate limiting and cost optimization
- Request caching and deduplication
- Unified monitoring and analytics
"""

import os
import asyncio
import hashlib
import json
import time
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
import requests


class ModelTier(Enum):
    """Model complexity tiers for automatic routing."""
    FAST = "fast"  # Quick tasks: Gemini Flash, Claude Haiku
    BALANCED = "balanced"  # Standard tasks: Gemini Pro, Claude Sonnet
    POWERFUL = "powerful"  # Complex tasks: Gemini Ultra, Claude Opus


class AntigravityAPIGateway:
    """
    Unified API Gateway for all AI model access through Antigravity.
    
    All agents and MCPs route through this gateway using a single API key.
    The gateway handles model selection, rate limiting, caching, and billing.
    """
    
    def __init__(self, api_key: Optional[str] = None, cache_dir: str = "artifacts/api_cache"):
        """
        Initialize the Antigravity API Gateway.
        
        Args:
            api_key: Antigravity API key (reads from ANTIGRAVITY_API_KEY if not provided)
            cache_dir: Directory for response caching
        """
        self.api_key = api_key or os.getenv("ANTIGRAVITY_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Request tracking for rate limiting
        self.request_history: List[Dict[str, Any]] = []
        self.rate_limit_window = 60  # seconds
        self.max_requests_per_minute = 60
        
        # Cost tracking
        self.total_cost = 0.0
        self.request_count = 0
        
        # Model configuration
        self.model_config = {
            ModelTier.FAST: {
                "gemini": "gemini-2.0-flash-exp",
                "claude": "claude-3-haiku-20240307",
                "openai": "gpt-4o-mini",
                "cost_per_1k_tokens": 0.0001
            },
            ModelTier.BALANCED: {
                "gemini": "gemini-2.0-pro",
                "claude": "claude-3-5-sonnet-20241022",
                "openai": "gpt-4o",
                "cost_per_1k_tokens": 0.001
            },
            ModelTier.POWERFUL: {
                "gemini": "gemini-exp-1206",
                "claude": "claude-opus-4-20250514",
                "openai": "gpt-4-turbo",
                "cost_per_1k_tokens": 0.01
            }
        }
        
        print(f"🌐 Antigravity API Gateway initialized")
        print(f"   API Key: {self.api_key[:10]}...{self.api_key[-4:] if self.api_key and len(self.api_key) > 14 else 'NOT_SET'}")
        print(f"   Cache: {self.cache_dir}")
    
    def _get_cache_key(self, prompt: str, model_tier: ModelTier, params: Dict[str, Any]) -> str:
        """Generate cache key for request."""
        content = f"{prompt}:{model_tier.value}:{json.dumps(params, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Check if response is cached."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                cached_data = json.loads(cache_file.read_text())
                cache_age = time.time() - cached_data.get("timestamp", 0)
                # Cache valid for 24 hours
                if cache_age < 86400:
                    return cached_data.get("response")
            except Exception:
                pass
        return None
    
    def _save_cache(self, cache_key: str, response: Dict[str, Any]):
        """Save response to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_data = {
            "timestamp": time.time(),
            "response": response
        }
        cache_file.write_text(json.dumps(cache_data, indent=2))
    
    def _check_rate_limit(self) -> bool:
        """Check if rate limit is exceeded."""
        current_time = time.time()
        # Remove old requests outside the window
        self.request_history = [
            req for req in self.request_history 
            if current_time - req["timestamp"] < self.rate_limit_window
        ]
        
        return len(self.request_history) < self.max_requests_per_minute
    
    def _record_request(self, model_tier: ModelTier, tokens: int):
        """Record request for rate limiting and cost tracking."""
        self.request_history.append({
            "timestamp": time.time(),
            "model_tier": model_tier.value,
            "tokens": tokens
        })
        
        self.request_count += 1
        cost = (tokens / 1000) * self.model_config[model_tier]["cost_per_1k_tokens"]
        self.total_cost += cost
    
    def select_model(
        self,
        task_complexity: ModelTier = ModelTier.BALANCED,
        provider_preference: Optional[str] = None
    ) -> str:
        """
        Select the best model for the task.
        
        Args:
            task_complexity: Complexity tier of the task
            provider_preference: Preferred provider (gemini, claude, openai)
            
        Returns:
            Model identifier string
        """
        if provider_preference and provider_preference in self.model_config[task_complexity]:
            return self.model_config[task_complexity][provider_preference]
        
        # Default to Gemini for Antigravity integration
        return self.model_config[task_complexity]["gemini"]
    
    def generate(
        self,
        prompt: str,
        model_tier: ModelTier = ModelTier.BALANCED,
        provider: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        use_cache: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using Antigravity API with automatic model selection.
        
        Args:
            prompt: Input prompt
            model_tier: Model complexity tier
            provider: Preferred provider (gemini, claude, openai)
            max_tokens: Maximum tokens to generate
            temperature: Generation temperature
            use_cache: Whether to use cached responses
            **kwargs: Additional model-specific parameters
            
        Returns:
            Response dictionary with text, model, tokens, cost
        """
        # Check rate limit
        if not self._check_rate_limit():
            raise Exception("Rate limit exceeded. Please wait before making more requests.")
        
        # Check cache
        params = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        cache_key = self._get_cache_key(prompt, model_tier, params)
        
        if use_cache:
            cached_response = self._check_cache(cache_key)
            if cached_response:
                print(f"✓ Using cached response (saved ${cached_response.get('cost', 0):.4f})")
                return cached_response
        
        # Select model
        model = self.select_model(model_tier, provider)
        
        # Route to appropriate API
        try:
            if "gemini" in model:
                response = self._call_gemini(prompt, model, max_tokens, temperature, **kwargs)
            elif "claude" in model:
                response = self._call_claude(prompt, model, max_tokens, temperature, **kwargs)
            elif "gpt" in model:
                response = self._call_openai(prompt, model, max_tokens, temperature, **kwargs)
            else:
                raise ValueError(f"Unknown model: {model}")
            
            # Record request
            tokens = response.get("usage", {}).get("total_tokens", len(prompt.split()) * 2)
            self._record_request(model_tier, tokens)
            
            result = {
                "text": response.get("text", ""),
                "model": model,
                "tokens": tokens,
                "cost": (tokens / 1000) * self.model_config[model_tier]["cost_per_1k_tokens"],
                "cached": False,
                "timestamp": datetime.now().isoformat()
            }
            
            # Cache response
            if use_cache:
                self._save_cache(cache_key, result)
            
            return result
            
        except Exception as e:
            print(f"❌ API call failed: {e}")
            return {
                "text": "",
                "error": str(e),
                "model": model,
                "cached": False
            }
    
    def _call_gemini(self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs) -> Dict[str, Any]:
        """Call Gemini API via Antigravity."""
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            
            return {
                "text": response.text if hasattr(response, 'text') else str(response),
                "usage": {
                    "total_tokens": len(prompt.split()) * 2  # Estimate
                }
            }
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
    
    def _call_claude(self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs) -> Dict[str, Any]:
        """Call Claude API via Antigravity (using OpenAI-compatible endpoint)."""
        # Antigravity provides unified endpoint for all models
        return self._call_openai_compatible(
            prompt, model, max_tokens, temperature, 
            base_url="https://api.antigravity.dev/v1",
            **kwargs
        )
    
    def _call_openai(self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs) -> Dict[str, Any]:
        """Call OpenAI API via Antigravity."""
        return self._call_openai_compatible(
            prompt, model, max_tokens, temperature,
            base_url="https://api.antigravity.dev/v1",
            **kwargs
        )
    
    def _call_openai_compatible(
        self, prompt: str, model: str, max_tokens: int, 
        temperature: float, base_url: str, **kwargs
    ) -> Dict[str, Any]:
        """Call OpenAI-compatible API endpoint."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "text": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {})
            }
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "total_requests": self.request_count,
            "total_cost": self.total_cost,
            "requests_last_minute": len(self.request_history),
            "cache_size": len(list(self.cache_dir.glob("*.json"))),
            "average_cost_per_request": self.total_cost / max(self.request_count, 1)
        }
    
    def clear_cache(self):
        """Clear all cached responses."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print(f"✓ Cleared {len(list(self.cache_dir.glob('*.json')))} cached responses")


# Global gateway instance
_gateway = None


def get_gateway() -> AntigravityAPIGateway:
    """Get or create global Antigravity API Gateway instance."""
    global _gateway
    if _gateway is None:
        _gateway = AntigravityAPIGateway()
    return _gateway


def generate_with_antigravity(
    prompt: str,
    complexity: str = "balanced",
    provider: Optional[str] = None,
    **kwargs
) -> str:
    """
    Convenience function to generate text using Antigravity API Gateway.
    
    Args:
        prompt: Input prompt
        complexity: Task complexity (fast, balanced, powerful)
        provider: Preferred provider (gemini, claude, openai)
        **kwargs: Additional parameters
        
    Returns:
        Generated text
    """
    gateway = get_gateway()
    tier = ModelTier(complexity)
    response = gateway.generate(prompt, model_tier=tier, provider=provider, **kwargs)
    return response.get("text", "")
