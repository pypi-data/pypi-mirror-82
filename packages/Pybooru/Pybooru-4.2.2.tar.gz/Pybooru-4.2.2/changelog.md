# Pybooru - Changelog

## Pybooru 4.2.2 - (2020-10-17)

- Added 504 error to HTTP_STATUS_CODE [#52](https://github.com/LuqueDaniel/pybooru/pull/52) by [@chlorofomduck](https://github.com/chlorofomduck)
- Fixed Danbooru client.favorite_remove() [#51](https://github.com/LuqueDaniel/pybooru/issues/51) and all 204 responses.

## Pybooru 4.2.0 - (2020-06-06)

**Note**: Pybooru 4.2.0 Is the last version that support Python 2.7

- Add support for Lolibooru [#44](https://github.com/LuqueDaniel/pybooru/pull/44) by [@Nachtalb](https://github.com/Nachtalb)
- Add support for safebooru.donmai.us to default sites [#37](https://github.com/LuqueDaniel/pybooru/pull/37) by [@mirukana](https://github.com/mirukana)
- Add `count_posts()` function to Danbooru API [#35](https://github.com/LuqueDaniel/pybooru/pull/35) by [@mirukana](https://github.com/mirukana)
- Replaced all `http` URLs for `https` [#36](https://github.com/LuqueDaniel/pybooru/pull/36) by [@mirukana](https://github.com/mirukana)
- Fixes the file url in the download example [#39](https://github.com/LuqueDaniel/pybooru/pull/39) by [@Luk3M](https://github.com/Luk3M)
- Fixes `Moebooru._build_hash_string`
- Small refactors
- Small fixes

## Pybooru 4.1.0 - (2017-02-08)

- Pybooru: refactored `_get_status()`
- Python 3.6 support
- Fixed `PybooruHTTPError`
- Pybooru: now `site_name` and `site_url` are `@property`
- Remove Pylint references
- End of Python 2.6 support
- Danbooru: added `post_mark_translated()`
- Danbooru: added `post_unvote()`
- Danbooru: added `post_flag_show()`
- Danbooru: added `post_appeals_show()`
- Danbooru: added `post_versions_show()`
- Danbooru: added `post_versions_undo()`
- Danbooru: added `comment_undelete()`
- Danbooru: added `comment_vote()`
- Danbooru: added `comment_unvote()`
- Danbooru: added `artist_undelete()`
- Danbooru: added `tag_show()`
- Danbooru: added `tag_udpate()`
- Danbooru: added `wiki_delete()`
- New docstring format
- Added support for Danbooru accounts levels.
- Refactored api_moebooru.py
- Code improvements
- Documentation improvement

## Pybooru 4.0.1 - (2016/12/09)

- Fix problems with Pypi

## Pybooru 4.0.0 - (2016/12/09)

- Added support to Danbooru
- Now Danbooru and Moebooru are two separed classes
- Pybooru has been refactored
- Moebooru (only): added support for API versioning
- Added PybooruAPIError exception
- Added **last_call** attribute to Danbooru and Moebooru to store last request information
- Examples has been updated
- Added **[documentation](http://pybooru.readthedocs.io/en/stable/)** to Pybooru (with Sphinx)
- Added some tools for Pybooru (tools folder)
- Refactored setup.py
- End of Python 3.2.x support
- Fixed parameter comparison (python 2.X only)
- In this version there's a nice amount of improvements

## Pybooru 3.0.1 - (2015/01/13)

- Minors changes

## Pybooru 3.0 - (2014/12/06)

- In this version there's a nice amount of code improvements
- Added compatibility with Python 3
- Pybooru now use requests
- Replace `"%s" % (foo)` for `"{0}".format(foo)`
- Improvement code style
- Added Travis CI to the project

## Pybooru 2.1.1 - (2013/12/26)

- Improve documentation style

## Pybooru 2.1 - (2013/10/14)

- Added login suppport for any Moebooru based site
- Fixed a bug: #c4b3435
- Added new information to setup.py
- Small changes
