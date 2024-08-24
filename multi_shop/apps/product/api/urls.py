from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'size', views.SizeView, basename='size')
router.register(r'color', views.ColorView, basename='color')
router.register(r'category', views.CategoryView, basename='category')
router.register(r'brand', views.BrandView, basename='brand')
router.register(r'offer', views.OfferView, basename='offer')
router.register(r'product', views.ProductView, basename='product')
router.register(r'image', views.ImageView, basename='image')
router.register(r'additional_information', views.AdditionalInformationView, basename='additional_information')
router.register(r'question_answer', views.QuestionAnswerView, basename='question_answer')
router.register(r'like', views.LikeView, basename='like')
router.register(r'comment', views.CommentView, basename='comment')
urlpatterns = router.urls
