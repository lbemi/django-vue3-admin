from rest_framework.routers import SimpleRouter

from school.views.school import SchoolViewSet, ProfessionalViewSet

router = SimpleRouter()
router.register("school", SchoolViewSet)
router.register("professional", ProfessionalViewSet)
urlpatterns = []

urlpatterns += router.urls
