from rest_framework.routers import SimpleRouter

from school.views.school import SchoolViewSet, ProfessionalViewSet

router = SimpleRouter()
router.register("api/school",  SchoolViewSet)
router.register("api/professional",  ProfessionalViewSet)
urlpatterns = []

urlpatterns += router.urls
