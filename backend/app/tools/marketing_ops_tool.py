"""Marketing Operations tool - content generation, scheduling, and calendar management."""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from openai import OpenAI
import json
from pathlib import Path


class MarketingOpsTool:
    """Tool for marketing operations: content generation, scheduling, repurposing."""
    
    def __init__(
        self,
        openai_api_key: str,
        openai_api_base: str,
        openai_model: str,
        workspace_path: str
    ):
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
        self.model = openai_model
        self.workspace = Path(workspace_path)
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def _call_llm(self, system: str, user: str, temperature: float = 0.7) -> str:
        """Call LLM for content generation."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=temperature,
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Content Generation
    
    def generate_linkedin_posts(
        self,
        topic: str,
        count: int = 30,
        tone: str = "professional",
        include_hooks: bool = True
    ) -> Dict[str, Any]:
        """Generate LinkedIn posts."""
        
        system = f"""You are a LinkedIn content strategist. Generate engaging, {tone} posts
that drive engagement and establish thought leadership."""

        user = f"""Generate {count} LinkedIn posts about: {topic}

Requirements:
- Each post should be 150-300 words
- Include engaging hooks if requested
- Mix of formats: insights, stories, questions, tips
- Use line breaks for readability
- No hashtags in main content (add separately)

Output as JSON array with this structure:
[
  {{
    "hook": "Opening line",
    "content": "Main post content",
    "cta": "Call to action",
    "hashtags": ["tag1", "tag2", "tag3"]
  }}
]
"""
        
        response = self._call_llm(system, user, temperature=0.8)
        
        try:
            # Extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            posts = json.loads(response[json_start:json_end])
            
            # Save to file
            output_file = self.workspace / f"linkedin_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(posts, f, indent=2)
            
            return {
                "success": True,
                "count": len(posts),
                "posts": posts,
                "file": str(output_file)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response}
    
    def generate_twitter_threads(
        self,
        topic: str,
        count: int = 10,
        tweets_per_thread: int = 5
    ) -> Dict[str, Any]:
        """Generate Twitter/X threads."""
        
        system = """You are a Twitter content expert. Create engaging threads that
educate, entertain, and drive engagement."""

        user = f"""Generate {count} Twitter threads about: {topic}

Each thread should have {tweets_per_thread} tweets.

Requirements:
- Tweet 1: Hook (grab attention)
- Tweets 2-{tweets_per_thread-1}: Value (insights, tips, stories)
- Final tweet: CTA + request for RT/follow
- Each tweet max 280 characters
- Use numbers, bullets, emojis strategically

Output as JSON array:
[
  {{
    "title": "Thread topic",
    "tweets": ["Tweet 1", "Tweet 2", ...]
  }}
]
"""
        
        response = self._call_llm(system, user, temperature=0.8)
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            threads = json.loads(response[json_start:json_end])
            
            output_file = self.workspace / f"twitter_threads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(threads, f, indent=2)
            
            return {
                "success": True,
                "count": len(threads),
                "threads": threads,
                "file": str(output_file)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response}
    
    def generate_blog_articles(
        self,
        topics: List[str],
        word_count: int = 1500,
        seo_optimized: bool = True
    ) -> Dict[str, Any]:
        """Generate long-form blog articles."""
        
        articles = []
        
        for topic in topics:
            system = """You are an expert content writer. Create comprehensive,
SEO-optimized articles that provide real value to readers."""

            user = f"""Write a {word_count}-word article about: {topic}

Requirements:
- Clear structure with H2 and H3 headings
- Include introduction and conclusion
- Use examples and actionable tips
- {"Include SEO keywords naturally" if seo_optimized else "Focus on readability"}
- Write in Markdown format

Output the complete article in Markdown.
"""
            
            content = self._call_llm(system, user, temperature=0.7)
            
            # Save article
            filename = topic.lower().replace(' ', '_')[:50]
            article_file = self.workspace / f"{filename}_{datetime.now().strftime('%Y%m%d')}.md"
            article_file.write_text(content, encoding='utf-8')
            
            articles.append({
                "topic": topic,
                "file": str(article_file),
                "word_count": len(content.split())
            })
        
        return {
            "success": True,
            "count": len(articles),
            "articles": articles
        }
    
    # Content Repurposing
    
    def repurpose_content(
        self,
        source_content: str,
        target_format: str,
        source_format: str = "article"
    ) -> Dict[str, Any]:
        """Repurpose content from one format to another."""
        
        format_instructions = {
            "linkedin": "5 LinkedIn posts (150-300 words each)",
            "twitter": "3 Twitter threads (5-7 tweets each)",
            "email": "Email newsletter (500-800 words)",
            "instagram": "10 Instagram captions (100-150 words each)",
            "short_video": "5 short video scripts (60-90 seconds each)",
        }
        
        if target_format not in format_instructions:
            return {"success": False, "error": f"Target format {target_format} not supported"}
        
        system = """You are a content repurposing expert. Transform content while
maintaining the core message and value."""

        user = f"""Repurpose this {source_format} into {format_instructions[target_format]}:

{source_content}

Requirements:
- Maintain key insights and value
- Adapt tone and length for the target platform
- Make each piece standalone (can be understood without the original)
- Include platform-specific best practices

Output as JSON with appropriate structure for {target_format}.
"""
        
        response = self._call_llm(system, user, temperature=0.7)
        
        try:
            json_start = response.find('{') if response.find('{') < response.find('[') else response.find('[')
            json_end = response.rfind('}') + 1 if response.rfind('}') > response.rfind(']') else response.rfind(']') + 1
            repurposed = json.loads(response[json_start:json_end])
            
            output_file = self.workspace / f"repurposed_{target_format}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(repurposed, f, indent=2)
            
            return {
                "success": True,
                "content": repurposed,
                "file": str(output_file)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response}
    
    # Content Calendar
    
    def create_content_calendar(
        self,
        start_date: datetime,
        duration_days: int = 60,
        posts_per_week: int = 5,
        platforms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a content calendar with scheduled posts."""
        
        platforms = platforms or ["linkedin", "twitter"]
        calendar = []
        
        current_date = start_date
        end_date = start_date + timedelta(days=duration_days)
        
        post_count = 0
        while current_date < end_date:
            # Skip weekends (optional)
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                for platform in platforms:
                    if post_count % len(platforms) == platforms.index(platform):
                        calendar.append({
                            "date": current_date.strftime("%Y-%m-%d"),
                            "time": "09:00",  # Default posting time
                            "platform": platform,
                            "status": "scheduled",
                            "content_id": None,  # To be filled with actual content
                        })
                        post_count += 1
                        
                        if post_count % 7 >= posts_per_week:
                            break
            
            current_date += timedelta(days=1)
        
        # Save calendar
        calendar_file = self.workspace / f"content_calendar_{start_date.strftime('%Y%m%d')}.json"
        with open(calendar_file, 'w') as f:
            json.dump(calendar, f, indent=2)
        
        return {
            "success": True,
            "total_posts": len(calendar),
            "calendar": calendar,
            "file": str(calendar_file)
        }
    
    def assign_content_to_calendar(
        self,
        calendar_file: str,
        content_file: str
    ) -> Dict[str, Any]:
        """Assign generated content to calendar slots."""
        
        try:
            # Load calendar
            with open(calendar_file) as f:
                calendar = json.load(f)
            
            # Load content
            with open(content_file) as f:
                content = json.load(f)
            
            # Assign content to calendar slots
            content_index = 0
            for slot in calendar:
                if slot["status"] == "scheduled" and content_index < len(content):
                    slot["content_id"] = content_index
                    slot["content"] = content[content_index]
                    content_index += 1
            
            # Save updated calendar
            output_file = calendar_file.replace('.json', '_with_content.json')
            with open(output_file, 'w') as f:
                json.dump(calendar, f, indent=2)
            
            return {
                "success": True,
                "assigned": content_index,
                "file": output_file
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Analytics and Optimization
    
    def analyze_top_performers(
        self,
        posts: List[Dict[str, Any]],
        metric: str = "engagement"
    ) -> Dict[str, Any]:
        """Analyze top-performing content to identify patterns."""
        
        # Sort by metric
        sorted_posts = sorted(
            posts,
            key=lambda x: x.get(metric, 0),
            reverse=True
        )
        
        top_10 = sorted_posts[:10]
        
        # Extract patterns using LLM
        system = """You are a content analytics expert. Analyze top-performing posts
to identify patterns, themes, and best practices."""

        user = f"""Analyze these top-performing posts and identify:
1. Common themes
2. Content structures that work
3. Tone and style patterns
4. Hook types that drive engagement
5. Recommendations for future content

Posts:
{json.dumps(top_10, indent=2)}

Provide actionable insights in JSON format.
"""
        
        response = self._call_llm(system, user, temperature=0.5)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            insights = json.loads(response[json_start:json_end])
            
            return {
                "success": True,
                "top_posts": top_10,
                "insights": insights
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response}
    
    def generate_content_variants(
        self,
        original_post: str,
        count: int = 5
    ) -> Dict[str, Any]:
        """Generate variants of a successful post for A/B testing."""
        
        system = """You are a copywriting expert. Create variations of content
that test different hooks, angles, and CTAs."""

        user = f"""Create {count} variations of this post:

{original_post}

Requirements:
- Test different hooks
- Try different content structures
- Vary the CTA
- Maintain core message

Output as JSON array of variants.
"""
        
        response = self._call_llm(system, user, temperature=0.9)
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            variants = json.loads(response[json_start:json_end])
            
            return {
                "success": True,
                "count": len(variants),
                "variants": variants
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response}
