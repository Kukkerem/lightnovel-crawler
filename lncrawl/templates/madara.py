import logging
from urllib.parse import urlencode

from bs4 import BeautifulSoup, Tag

from lncrawl.models import Chapter, SearchResult
from lncrawl.templates.soup.searchable import SearchableSoupTemplate
from lncrawl.templates.browser.chapter_only import ChapterOnlyBrowserTemplate

logger = logging.getLogger(__name__)


class MadaraTemplate(SearchableSoupTemplate, ChapterOnlyBrowserTemplate):
    is_template = True

    def initialize(self) -> None:
        self.cleaner.bad_tags.update(["h3"])
        self.cleaner.bad_css.update(['a[href="javascript:void(0)"]'])

    def select_search_items(self, query: str):
        params = dict(
            s=query,
            post_type="wp-manga",
            op="",
            author="",
            artist="",
            release="",
            adult="",
        )
        soup = self.get_soup(f"{self.home_url}?{urlencode(params)}")
        yield from soup.select(".c-tabs-item__content")

    def parse_search_item(self, tag: Tag) -> SearchResult:
        a = tag.select_one(".post-title h3 a")
        latest = tag.select_one(".latest-chap .chapter a").text
        votes = tag.select_one(".rating .total_votes").text
        return SearchResult(
            title=a.text.strip(),
            url=self.absolute_url(a["href"]),
            info="%s | Rating: %s" % (latest, votes),
        )

    def parse_title(self, soup: BeautifulSoup) -> str:
        tag = soup.select_one(".post-title h1")
        assert tag
        for span in tag.select("span"):
            span.extract()
        return tag.text.strip()

    def parse_cover(self, soup: BeautifulSoup) -> str:
        tag = soup.select_one(".summary_image a img")
        if isinstance(tag, Tag):
            if tag.has_attr("data-src"):
                return self.absolute_url(tag["data-src"])
            if tag.has_attr("src"):
                return self.absolute_url(tag["src"])
        return ""

    def parse_authors(self, soup: BeautifulSoup):
        for a in soup.select('.author-content a[href*="manga-author"]'):
            yield a.text.strip()

    def parse_genres(self, soup):
        for a in soup.select('.genres-content a[rel="tag"]'):
            yield a.text.strip()

    def parse_summary(self, soup):
        possible_summary = soup.select_one(".description-summary a")
        return self.cleaner.extract_contents(possible_summary)

    def select_chapter_tags(self, soup: BeautifulSoup):
        try:
            clean_novel_url = self.novel_url.split("?")[0].strip("/")
            response = self.submit_form(f"{clean_novel_url}/ajax/chapters/")
            soup = self.make_soup(response)
            chapters = soup.select("ul.main .wp-manga-chapter a")
            yield from reversed(chapters)
            use_alternate = True
        except Exception as e:
            use_alternate = True
            logger.debug("Failed to fetch chapters using ajax", e)

        if use_alternate:
            nl_id = soup.select_one("#manga-chapters-holder[data-id]")
            if not isinstance(nl_id, Tag):
                logger.debug("No chapter id tag found for alternate method")
                return
            try:
                response = self.submit_form(
                    f"{self.home_url}wp-admin/admin-ajax.php",
                    data={
                        "action": "manga_get_chapters",
                        "manga": nl_id["data-id"],
                    },
                )
                soup = self.make_soup(response)
                chapters = soup.select("ul.main .wp-manga-chapter a")
                yield from reversed(chapters)
            except Exception as e:
                logger.debug("Failed to fetch chapters using alternate method", e)

    def parse_chapter_item(self, tag: Tag, id: int) -> Chapter:
        return Chapter(
            id=id,
            title=tag.text.strip(),
            url=self.absolute_url(tag["href"]),
        )

    def select_chapter_body(self, soup: BeautifulSoup) -> Tag:
        return soup.select_one("div.reading-content")
