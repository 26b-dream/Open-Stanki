from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Third Party
    from bs4.element import ResultSet

# Third Party
from bs4 import BeautifulSoup
from bs4.element import Tag as Tag


class StrictBeautifulSoupFaiure(Exception):
    pass


# Because of the way BS4 is designed I have to monkey patch the features into Tag and BeautifulSoup
# Creating a new class will return original Tag objects that do not have the extra functions
# This will overwrite the original Tag and BeautifulSoup classes
# The alternative is digging into how Tag objects are created and replacing them, but it's not worth the time
class _Tag(Tag):
    def strict_select(self: Tag, selector: str) -> ResultSet[Tag]:
        """Same as .select but it will raise an exception if no match is found"""
        output = self.select(selector)
        if len(output) == 0:
            raise StrictBeautifulSoupFaiure(f"No matches found for strict_select({selector})")
        else:
            return output  # type: ignore - monkey patching causes Tag and _Tag issues

    def strict_select_one(self: Tag, selector: str) -> Tag:
        """Same as .select but it will raise an exception the number of matches is not 1"""
        output = self.select(selector)
        number_of_matches = len(output)
        if number_of_matches == 1:
            return output[0]  # type: ignore - monkey patching causes Tag and _Tag issues]
        else:
            raise StrictBeautifulSoupFaiure(
                f"Wrong number of matches found for strict_select({selector}), found {number_of_matches}"
            )

    def strict_get_str(self: Tag, key: str) -> str:
        pass
        """Same as .get but it will raise an exception if no match is found"""
        output = self.get(key)
        if isinstance(output, str) or isinstance(output, list):
            return output
        if isinstance(output, list):
            return " ".join(output)
        else:
            string = f"No matches found for strict_get_str({key})"
            raise StrictBeautifulSoupFaiure(string)


# Actually add functions to Tag
# Because the type hints say the return type is Tag the type hints need to be added to typings\bs4\element.pyi
# ! For these to work properly type hints need to be added to element.pyi in
# class Tag:
#   def strict_select(self, selector: str) -> ResultSet[Tag]: ...
#   def strict_select_one(self, selector: str) -> Tag: ...
#   def strict_get_str(self, key: str) -> str: ...
Tag.strict_select_one = _Tag.strict_select_one
Tag.strict_select = _Tag.strict_select
Tag.strict_get_str = _Tag.strict_get_str

BeautifulSoup.strict_select_one = Tag.strict_select_one
BeautifulSoup.strict_select = Tag.strict_select
BeautifulSoup.strict_get_str = Tag.strict_get_str
