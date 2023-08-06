from asyncio import AbstractEventLoop
from typing import List, Optional, Union

from .booru import Booru, BooruImage

API_URL = "https://danbooru.donmai.us/"


class DanbooruImage(BooruImage):

    def __init__(self, iid, data_dict):
        super().__init__(iid, data_dict)

    @property
    def sample_url(self):
        return self._data_dict.get("large_file_url", "")

    @property
    def tags(self):
        return self._data_dict.get("tag_string", "")

    @property
    def thumbnail_url(self) -> str:
        return self._data_dict.get("preview_file_url", "")


class Danbooru(Booru):
    """
    Wrap API of danbooru (https://danbooru.donmai.us/)

    See also: https://danbooru.donmai.us/wiki_pages/help:api

    Example:

    ```
    danbooru = Danbooru(username="username", api_key="your-api-key")
    danbooru.get_posts(limit=10, tags="yazawa_niko*")
    ```

    Note: Danbooru recommands to test script on https://testbooru.donmai.us

    You can specify the url when you are creating an instance

    ```
    danbooru = Danbooru(api_url="https://testbooru.donmai.us")
    danbooru.get_posts()
    ```

    """

    def __init__(
        self,
        user: str = None,
        token: str = None,
        root_url: str = API_URL,
        proxy: Optional[str] = None,
        loop: Optional[AbstractEventLoop] = None,
    ):
        """Create an instance of Danbooru.

        The default URL root is https://danbooru.donmai.us/ .

        You can also specify other URL by passing `root_url` parameter.

        Args:
            user (str, optional): User name/id of danbooru. Defaults to None.
            token (str, optional): API Key of danbooru. Defaults to None.
            root_url (str, optional): API URL root. Defaults to API_URL.
            loop (Optional[AbstractEventLoop], optional): EventLoop. Defaults to None.
        """
        super(Danbooru, self).__init__(user=user,
            token=token,
            root_url=root_url,
            proxy=proxy,
            loop=loop)

    async def get_post(self, id: str) -> Union[DanbooruImage, None]:
        """Get a specific post by id.
        API: /posts/$id.json (when $id is the post id)

        Args:
            id (str): The post id

        Returns:
            Union[DanbooruImage, None]: DanbooruImage
        """
        params = {
            # api key
            "login": self.user,
            "api_key": self.token,
        }

        code, response = await self._get(self.root_url + f"/posts/{id}.json",
            params=params)

        if code == 404:
            # found nothing so return None
            return None

        return DanbooruImage(str(response.get("id")), response)

    async def get_posts(
        self,
        tags: str = "",
        page: int = None,
        limit: int = None,
        md5: str = None,
        random: bool = True,
        raw: bool = False,
        **kwargs,
    ) -> List[DanbooruImage]:
        """Get a list of posts. API: /posts.json

        Args:
            tags (str, optional): The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags. Defaults to "".
            page (int, optional): The page number. Defaults to None.
            limit (int, optional): How many posts you want to retrieve. Defaults to None.
            md5 (str, optional): The md5 of the image to search for. Defaults to None.
            random (bool, optional): Can be: true, false Defaults to True.
            raw (bool, optional): When this parameter is set the tags parameter will not be parsed for aliased tags, metatags or multiple tags, and will instead be parsed as a single literal tag. Defaults to False.

        Returns:
            List[DanbooruImage]: a list contains `DanbooruImage`
        """

        params = {
            "tags": tags,
            "random": 1 if random else 0,
            "raw": 1 if raw else 0,
            # api key
            "login": self.user,
            "api_key": self.token,
            # other possible parameters
            "page": page,
            "limit": limit,
            "md5": md5,
        }

        code, response = await self._get(
            self.root_url + "/posts.json",
            params=params,
            **kwargs,
        )

        res_list = list()
        for i in response:
            # some post may lacks "id" property,
            # just ignore them
            if not i.get("id", None):
                continue
            res_list.append(DanbooruImage(str(i.get("id")), i))
        return res_list
