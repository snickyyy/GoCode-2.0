import math

from fastapi import HTTPException


class Pagination:
    def __init__(self, total_items: int, page_size: int):
        self.total_items = total_items
        self.page_size = page_size

    @property
    def total_items(self):
        return self._total_items

    @total_items.setter
    def total_items(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Total items must be a non-negative integer")
        self._total_items = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Page size must be a positive integer")
        self._page_size = value

    @property
    def total_pages(self):
        return math.ceil(self.total_items / self.page_size) if math.ceil(self.total_items / self.page_size) else 1

    def validate_page(self, page: int):
        if not isinstance(page, int) or page <= 0:
            raise HTTPException(status_code=409, detail="Page must be a positive integer")
        elif page > self.total_pages and page != 1:
            raise HTTPException(status_code=404, detail="Not Found")

    @staticmethod
    def has_previous(page: int):
        return page > 1

    def has_next(self, page: int):
        self.validate_page(page)
        return page < self.total_pages

    def next_page(self, page: int):
        if self.has_next(page):
            return page + 1
        return None

    def previous_page(self, page: int):
        if self.has_previous(page):
            return page - 1
        return None

    @property
    def page_range(self):
        return range(1, self.total_pages + 1)

    def get_offset_and_limit(self, page: int):
        self.validate_page(page)
        offset = (page - 1) * self.page_size
        limit = self.page_size
        return offset, limit