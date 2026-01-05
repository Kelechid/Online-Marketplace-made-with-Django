# item/recommendations.py
from collections import Counter
from .models import Item

def recommend_items(user):
    if not user.is_authenticated:
        return Item.objects.none()

    purchased_item_ids = []

    # Puddle usually has Order / OrderItem
    for order in user.orders.all():
        for order_item in order.items.all():
            purchased_item_ids.append(order_item.item.id)

    related = Counter()

    for item_id in purchased_item_ids:
        item = Item.objects.get(id=item_id)
        similar_items = Item.objects.filter(
            category=item.category
        ).exclude(id__in=purchased_item_ids)

        related.update(similar_items.values_list('id', flat=True))

    recommended_ids = [i for i, _ in related.most_common(4)]
    return Item.objects.filter(id__in=recommended_ids)
