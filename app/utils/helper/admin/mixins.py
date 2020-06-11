class ToggleActiveMixin:
    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{}건의 선택을 Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = '선택한 것들을 Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{}건의 선택을 Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = '선택한 것들을 Deactivate 상태로 변경'
