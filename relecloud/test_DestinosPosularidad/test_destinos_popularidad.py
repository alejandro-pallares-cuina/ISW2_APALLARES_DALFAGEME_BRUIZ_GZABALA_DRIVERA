from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg

from relecloud import models


class PopularityMetricTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='pass')

    def annotate_popularity(self):
        return (
            models.Destination.objects
            .annotate(reviews_count=Count('reviews'), avg_rating=Avg('reviews__rating'))
            .annotate(popularity_score=models.popularity_score_expression())
        )

    def test_popularity_metric_values(self):
        # Destinations
        d1 = models.Destination.objects.create(name='D1', description='d1')
        d2 = models.Destination.objects.create(name='D2', description='d2')
        d3 = models.Destination.objects.create(name='D3', description='d3')

        # Reviews: d1 -> two 5s, d2 -> one 4, d3 -> none
        models.Review.objects.create(user=self.user, destination=d1, rating=5)
        models.Review.objects.create(user=self.user, destination=d1, rating=5)
        models.Review.objects.create(user=self.user, destination=d2, rating=4)

        qs = self.annotate_popularity().filter(name__in=['D1', 'D2', 'D3']).order_by('name')
        data = {obj.name: obj.popularity_score for obj in qs}

        # Expected values: D1 -> 2*0.6 + 5*0.4 = 1.2 + 2.0 = 3.2
        # D2 -> 1*0.6 + 4*0.4 = 0.6 + 1.6 = 2.2
        # D3 -> 0
        self.assertAlmostEqual(data['D1'], 3.2, places=4)
        self.assertAlmostEqual(data['D2'], 2.2, places=4)
        self.assertAlmostEqual(data['D3'], 0.0, places=4)

    def test_popularity_ordering_top(self):
        # Create several destinations with different scores
        for i in range(1, 6):
            models.Destination.objects.create(name=f'D{i}', description=f'd{i}')

        # D1: high avg (5), 1 review -> score 0.6+2.0=2.6
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D1'), rating=5)
        # D2: two reviews 4,4 -> count2 avg4 -> 2*0.6 +4*0.4 =1.2+1.6=2.8 (should be top)
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D2'), rating=4)
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D2'), rating=4)
        # D3: one review 3 -> 0.6 + 1.2 = 1.8
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D3'), rating=3)
        # D4: no reviews -> 0
        # D5: three reviews 2,2,2 -> count3 avg2 -> 3*0.6 +2*0.4 =1.8+0.8=2.6
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D5'), rating=2)
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D5'), rating=2)
        models.Review.objects.create(user=self.user, destination=models.Destination.objects.get(name='D5'), rating=2)

        ordered = list(self.annotate_popularity().order_by('-popularity_score'))
        ordered_names = [d.name for d in ordered]

        # D2 (2.8) should be first
        self.assertEqual(ordered_names[0], 'D2')
        # Ensure ordering is non-increasing by score
        scores = [d.popularity_score for d in ordered]
        for a, b in zip(scores, scores[1:]):
            self.assertGreaterEqual(a, b)
