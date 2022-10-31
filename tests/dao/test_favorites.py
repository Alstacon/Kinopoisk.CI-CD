# import pytest
#
# from project.dao import FavoritesDAO
# from project.models import Favorites
#
#
# class TestFavoritesDAO:
#     @pytest.fixture
#     def favorites_dao(self, db):
#         return FavoritesDAO(db.session)
#
#     @pytest.fixture
#     def favorite_1(self, db):
#         f = Favorites(user_id=1, movie_id=1)
#         db.session.add(f)
#         db.commit()
#         return f
#
#     def test_add_favorites(self, favorites_dao):
#         favorite = {
#             "user_id": 2,
#             "movie_id": 1
#         }
#         new_fav = favorites_dao.create(favorite)
#         assert new_fav.user_id == favorite.get("user_id")
#
#
#
