# class TravelFilter(filters.):
#     travellers = filters.NumberFilter(field_name="travellers", lookup_expr="exact")
#     # admin = filters.CharFilter(field_name="admin__user_name", lookup_expr="icontains")
#     # destination = filters.CharFilter(field_name="destination", lookup_expr='exact')
#     # start_place = filters.CharFilter(field_name="start_place", lookup_expr='exact')
#     # transportation = filters.CharFilter(field_name="transportation",lookup_expr='exact')
#     # mode = filters.ChoiceFilter(
#     #     field_name="mode", choices=Travel.type_choices, required=False
#     # )
#     class Meta:
#         model = Travel
#         # fields = ["travellers","admin", "destination", "transportation",'mode']
#         fields=['travellers']
