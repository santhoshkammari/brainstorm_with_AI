import asyncio
import re
from typing import List

from researcher_ai.main.search_provider.base import Searcher


class GoogleSearch(Searcher):
    def perform_search(self, query: str) -> List[str]:
        # Here you'd implement the actual API search using google_searcher
        print(f"Searching Google for: {query}")
        return [f"Result {i + 1} for {query}" for i in range(5)]  # Dummy results

    def perform_batch_search(self, batch_queries: List[str]) -> List[str]:
        pass

import asyncio
from typing import List
from opengenai.web_search import OptimizedMultiQuerySearcher

class RealTimeGoogleSearchProvider(Searcher):
    def __init__(self, search_provider="google"):
        self.search_provider = search_provider
        self.searcher = OptimizedMultiQuerySearcher()

    def perform_search(self, query: str,max_urls=5) -> List[str]:
        return self.searcher.search_single_query(query,search_provider=self.search_provider).urls[:max_urls]


    async def _async_batch_search(self, batch_queries,max_urls=5) -> List[str]:
        all_urls = await self.searcher.search_multiple_queries(
            queries=batch_queries,
            search_provider=self.search_provider
        )
        all_urls = [url.urls for url in all_urls]
        filtered_urls = [y for x in zip(*all_urls) for y in x]
        filtered_urls = [self.extract_until_hash(x) if self.is_hash(x) else x for x in filtered_urls]
        filtered_urls = [_ for _ in filtered_urls if _]
        return filtered_urls[:max_urls]

    def perform_batch_search(self, batch_queries,max_urls=5) -> List[str]:
        return asyncio.run(self._async_batch_search(batch_queries,max_urls=max_urls))

    def is_hash(self, x):
        return '#' in x

    def extract_until_hash(self, x):
        results = re.findall(r'(.*)#',x)
        if results:
            return results[0]
        return ""