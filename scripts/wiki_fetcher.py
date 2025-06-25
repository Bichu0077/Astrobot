import wikipediaapi
from typing import Optional, Dict


import wikipediaapi


class WikiFetcher:
    def __init__(self, language: str = "en", user_agent: str = None):
        """
        Initialize the Wikipedia API client.

        Args:
            language (str): Wikipedia language (default = 'en').
            user_agent (str): Custom user-agent string.
        """
        self.wiki = wikipediaapi.Wikipedia(
            language=language,
            user_agent=user_agent
        )


    def fetch_page(self, title: str) -> dict:
        page = self.wiki.page(title)
        if not page.exists():
            # Fallback to best match using search
            search_result = self.wiki.search(title)
            if search_result:
                fallback = search_result[0]
                page = self.wiki.page(fallback)
                if not page.exists():
                    return {}
                return {
                    "title": fallback,
                    "full_text": page.text,
                    "url": page.fullurl,
                }
            return {}
        return {
            "title": title,
            "full_text": page.text,
            "url": page.fullurl,
        }

    def _get_full_text(self, page: wikipediaapi.WikipediaPage) -> str:
        """
        Recursively fetch full text including all sub-sections of a page.

        Args:
            page (WikipediaPage): Wikipedia page object.

        Returns:
            str: Full page content.
        """
        content = [page.summary]
        self._fetch_sections_recursive(page.sections, content)
        return "\n\n".join(content)

    def _fetch_sections_recursive(self, sections, content):
        for section in sections:
            if section.text.strip():
                content.append(f"{section.title}\n{section.text.strip()}")
            if section.sections:
                self._fetch_sections_recursive(section.sections, content)
